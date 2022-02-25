import sys, os
from os.path import join, getsize

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time

from tqdm import tqdm

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator
import pyvisa

rm = pyvisa.ResourceManager()
instSonde = WrapperEMRFeldsonde('ASRL3::INSTR', rm)
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR', rm)
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR', rm)
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR', rm)
sys.path.append('gui')

class External_FS_test(QThread):
    completedflag = pyqtSignal(bool, int)
    countChanged = pyqtSignal(float, float, float, float, int)
    positionChanged = pyqtSignal(int)  # emit the current calibration position

    def __init__(self, StartFreq, FreqStep, MaxFreq, E_T, startAPM, Position):
        super(External_FS_test, self).__init__()
        self.StartFreq = StartFreq
        self.FreqStep = FreqStep
        self.MaxFreq = MaxFreq
        self.position = Position
        self.E_T = E_T
        self.E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
        self.E_L_Tol = 0.6
        self.startAPM = startAPM
        self.stopped = False
        self.completed = False
        self.restart = False
        self.isPaused = False
        self.isWaiting = False
        # Resource adresses
        self.activSwitch = 0


        # dummy value
        self.testFreq = 0
        self.vorPower = 0
        self.bwdPow = 0
        self.FieldStrength = 0

    def run(self):
        while self.position in range(6):
            self.stopped = False
            self.completed = False
            setFrequ = self.StartFreq
            setAPM = self.startAPM
            currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
            if currAmpSwitch == 1:
                instSwitch.switchAmp1()
                activSwitch = 1
                print('activeSwitch: %i ' % self.activSwitch )
            elif currAmpSwitch == 2:
                instSwitch.switchAmp2()
                activSwitch = 2
                print('activeSwitch: %i' % self.activSwitch )
            elif currAmpSwitch == 3:
                instSwitch.switchAmp3()
                activSwitch = 3
                print('activeSwitch: %i ' % self.activSwitch )
            elif currAmpSwitch == 4:
                print('activeSwitch Abort: %i ' % self.activSwitch )
                break

            frequList = []
            while setFrequ <= self.MaxFreq:
                frequList.append(setFrequ)
                setFrequ = setFrequ * 1.01

            for i in tqdm(frequList, desc="Calibration Frequ Step:"):
                setFrequ = i
                MV = setAPM
                instSigGen.switchRFOff()  # set RF ON!!!!!!!!!
                controller = PI(0.2, 0.033, MV, 1)
                controller.send(None)
                # check if the switch needs to be switched
                currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
                if currAmpSwitch != activSwitch:
                    if currAmpSwitch == 1:
                        instSwitch.switchAmp1()
                        activSwitch = 1
                        print('activeSwitch: %i' % activSwitch)
                    elif currAmpSwitch == 2:
                        instSwitch.switchAmp2()
                        activSwitch = 2
                        print('activeSwitch: %i' % activSwitch)
                    elif currAmpSwitch == 3:
                        instSwitch.switchAmp3()
                        activSwitch = 3
                        print('activeSwitch: %i' % activSwitch)
                    elif currAmpSwitch == 4:
                        print('activeSwitch Abort: %i' % activSwitch)
                        abortTest()
                        break
                instSigGen.setFrequMHZ(setFrequ)  # Set Beginning frequency
                # if setAPM > maxAPMPoss:
                #     abortTest()
                instSigGen.setAmpDBM(setAPM)  # set beginning amplitude value
                instSigGen.switchRFOn()  # set RF ON!!!!!!!!

                instSonde.readval()
                currSondeVal = instSonde.effEVal
                instPowerMeter.switchChannelA()
                instPowerMeter.getMeasVal()
                currFwdVal = instPowerMeter.currVal
                instPowerMeter.switchChannelB()
                instPowerMeter.getMeasVal()
                currRevVal = instPowerMeter.currVal

                k = 1
                startTime = time.time()
                iRow = 1
                tmpSondeVal = [False] * 3
                while 1:
                    # quadrieren der toleranzen -> kein sqrt nötig
                    if (self.E_T < currSondeVal < max_E_L):
                        # find at least 3 Sondeval in Row to validate
                        tmpSondeVal[iRow] = True
                    else:
                        tmpSondeVal[iRow] = False

                    # print(tmpSondeVal)
                    iRow = iRow + 1
                    if iRow > 2:
                        iRow = 0

                    if all(tmpSondeVal):
                        break

                    if (k % 60) == 0:
                        continueTest = input('Continue Test?\n')
                        if continueTest == 'No':
                            abortTest()
                    # Check if Rev and FWD are nearly same
                    if abs(abs(currFwdVal) - abs(currRevVal)) <= powMeterTol:
                        print('tolerance fwd and reverse broken with %f' % abs(abs(currFwdVal) - abs(currRevVal)))
                        abortTest()
                        break
                    # if currSondeVal < max_E_L:
                    #     setAPM = setAPM + stepAPM
                    # else:
                    #     setAPM = setAPM - stepAPM
                    # print('updated APMval: %f \n' % setAPM)

                    # if setAPM > maxAPMPoss:
                    #     abortTest()

                    # piyes = input('set MV TO APM?')
                    # if piyes == 'yes':
                    #     print('set APM to %f' % MV)
                    # print('set APM to %f' % MV)
                    setAPM = MV

                    if abs(abs(prevStepAPM) - abs(setAPM)) > maxChangeVal:
                        print('APM TO BIG')
                        abortTest()

                    instSigGen.setAmpDBM(setAPM)
                    instSigGen.switchRFOn()  # set RF ON!!!!!!!!!
                    # update measured val
                    timeSonde = time.time()
                    instSonde.readval()
                    currSondeVal = instSonde.effEVal
                    # print('time sonde:%f' % (time.time()-timeSonde))
                    # print('Updated currSondeVal: %f ' % currSondeVal)
                    t = time.time() - startTime
                    MV = controller.send([t, currSondeVal, control_E_L])
                    if (k > 5) and ((k % 3) == 0):
                        timePowMetA = time.time()
                        instPowerMeter.switchChannelA()
                        instPowerMeter.getMeasVal()
                        currFwdVal = instPowerMeter.currVal
                        # print('time PowerMeterA:%f' % (time.time()-timePowMetA))
                        # print('Updated CurrFwdVal: %f \n' % currFwdVal)
                        timePowMetB = time.time()
                        instPowerMeter.switchChannelB()
                        instPowerMeter.getMeasVal()
                        currRevVal = instPowerMeter.currVal
                        # print('time PowerMeterB:%f' % (time.time()-timePowMetB))
                    # print('Updated currRevVal: %f \n' % currRevVal)
                    k = k + 1
                    plt.scatter(k, currSondeVal)
                    plt.show()
                    plt.pause(0.001)
                prevStepAPM = setAPM

                # save the values in lists
                instPowerMeter.switchChannelA()
                instPowerMeter.getMeasVal()
                currFwdVal = instPowerMeter.currVal
                instPowerMeter.switchChannelB()
                instPowerMeter.getMeasVal()
                currRevVal = instPowerMeter.currVal
                instSonde.readval()
                currSondeVal = instSonde.effEVal
                controller.close()
                frequVal.append(setFrequ)
                powFwdVal.append(currFwdVal)
                powRevVal.append(currRevVal)
                sondeListVal.append(currSondeVal)
                powAPMSet.append(setAPM)
                plt.savefig('graphs/Field_strength_%s_%i_%i' % (polarisation, currPoint, ii))
                plt.close()
                # print('Saved currFwdVal: %f' % currFwdVal)
                res = [l for l in zip(frequVal, powFwdVal, powRevVal, powAPMSet, sondeListVal)]
                path = 'output_%s_%i.csv' % (polarisation, currPoint)
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for l in res:
                        writer.writerow(l)
                ii = ii + 1





        #####
        # rewrite
        print('StartFreq %s' % self.StartFreq)
        print('FreqStep %s' % self.FreqStep)
        print('MaxFreq %s' % self.MaxFreq)
        print('E_T %s' % self.E_T)
        print('startAPM %s' % self.startAPM)
        print('position %s' % self.position)

            self.testFreq = self.StartFreq
            position = self.position
            while self.testFreq < self.MaxFreq:
                self.vorPower = self.vorPower + 0.01
                self.bwdPow = self.vorPower - 2
                self.FieldStrength = self.FieldStrength + 0.04
                print("testFreq %s" % self.testFreq)
                print("freq step %s" % self.FreqStep)
                print("position %s" % self.position)
                measuredFreq = self.testFreq
                vorPower = self.vorPower
                bwdPow = self.bwdPow
                FieldStrength = self.FieldStrength
                self.testFreq = self.testFreq + self.FreqStep * self.testFreq
                ######
                # emit the data to GUI
                self.countChanged.emit(measuredFreq, vorPower, bwdPow, FieldStrength, position)

                #
                # time.sleep(0.01)
                while self.isPaused:
                    time.sleep(0)
                if self.stopped:
                    break
            if not self.stopped:
                self.completed = True
                completed = self.completed
                self.completedflag.emit(completed, position)

            self.isWaiting = True  # set isWaiting True to wait change of the position

            # waite for input 'Fortfahren'
            while self.isWaiting:
                time.sleep(0)

            self.position += 1
            print(self.position)

    def stop(self):
        # print("thread stoped")
        self.stopped = True

    def pause(self):
        self.isPaused = True

    def resum(self):
        self.isPaused = False

    def runNextTest(self):
        self.isWaiting = False


    def abortTest():
        instSigGen.switchRFOff()
        instSwitch.reset()
        print('Test Aborted')
        sys.exit()


    def checkValues(gridValFrequ, gridValFwd):
        isvalid = []
        crntDbms = []
        cntFrequ = len(gridValFwd[1])
        for iFrequ in range(cntFrequ):
            maxDiff = 0
            crntDbms.clear()
            for i in range(len(gridValFwd)):
                crntDbms.append(gridValFwd[i][iFrequ])
            minVal = min(crntDbms)
            maxVal = max(crntDbms)
            maxDiff = abs(minVal - maxVal)
            if maxDiff > 6:
                isvalid.append(0)
            else:
                isvalid.append(1)


    def PI(Kp, Ki, MV_bar, beta):
        # initialize stored data
        t_prev = -1
        I = 0

        # initial control
        MV = MV_bar

        while True:
            # yield MV, wait for new t, SP, PV
            t, PV, SP = yield MV

            # PI calculations
            P = Kp * (beta * SP - PV)
            I = I + Ki * (SP - PV) * (t - t_prev)
            # print('P: %f' % P)
            # print('I: %f' % I)
            MV = MV_bar + P + I

            # print('New MV: %f' % MV)
            # update stored data for next iteration
            t_prev = t
