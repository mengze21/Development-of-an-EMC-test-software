import sys, os
from os.path import join, getsize

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time
import csv
from csv import reader

from tqdm import tqdm

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator
from calibrationFileCreate import createCalibrationFile
import pyvisa

sys.path.append('gui')


class External_FS_test(QThread):
    completedflag = pyqtSignal(bool, int)
    countChanged = pyqtSignal(float, float, float, float, int)
    positionChanged = pyqtSignal(int)  # emit the current calibration position



    def __init__(self, StartFreq, FreqStep, MaxFreq, E_T, startAPM, Position, Polarisation):
        super(External_FS_test, self).__init__()
        self.StartFreq = StartFreq
        self.FreqStep = FreqStep
        self.MaxFreq = MaxFreq
        self.position = Position
        self.E_T = E_T
        self.E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
        self.E_L_Tol = 0.6 #Field Strength Toleranz
        self.polarisation = Polarisation # Polarisation auch aus GUI
        self.max_E_L = self.E_L + self.E_L_Tol
        self.control_E_L = self.E_L + self.E_L_Tol / 2

        self.startAPM = startAPM
        self.powMeterTol = 0.1 #eventuell aus GUI
        self.stopped = False
        self.completed = False
        self.restart = False
        self.isPaused = False
        self.isWaiting = False
        # Resource adresses
        self.activSwitch = 0

        rm = pyvisa.ResourceManager()
        self.instSonde = WrapperEMRFeldsonde('ASRL3::INSTR', rm)
        self.instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR', rm)
        self.instSwitch = WrapperSwitchHP('GPIB0::9::INSTR', rm)
        self.instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR', rm)


        # dummy value
        self.testFreq = 0
        self.vorPower = 0
        self.bwdPow = 0
        self.FieldStrength = 0

    def run(self):
        prevStepAPM = self.startAPM
        # list creation
        frequVal = []
        powFwdVal = []
        sondeListVal = []
        gridValFrequ = []
        gridValFwd = []
        powRevVal = []
        powAPMSet = []
        # list CSV fiel
        listCsvFile = []
        while self.position in range(6):
            self.stopped = False
            self.completed = False
            setFrequ = self.StartFreq
            setAPM = self.startAPM
            currAmpSwitch = self.instSwitch.validFrequ(setFrequ)  # check if frequency is valid
            if currAmpSwitch == 1:
                self.instSwitch.switchAmp1()
                self.activSwitch = 1
                print('activeSwitch: %i ' % self.activSwitch )
            elif currAmpSwitch == 2:
                self.instSwitch.switchAmp2()
                self.activSwitch = 2
                print('activeSwitch: %i' % self.activSwitch )
            elif currAmpSwitch == 3:
                self.instSwitch.switchAmp3()
                self.activSwitch = 3
                print('activeSwitch: %i ' % self.activSwitch )
            elif currAmpSwitch == 4:
                print('activeSwitch Abort: %i ' % self.activSwitch )
                break

            frequList = []
            while setFrequ <= self.MaxFreq:
                frequList.append(setFrequ)
                setFrequ = setFrequ * 1.01

            for i in tqdm(frequList, desc="Calibration Frequ Step:"):
                if self.stopped:
                    break
                setFrequ = i
                MV = setAPM
                self.instSigGen.switchRFOff()  # set RF ON!!!!!!!!!
                controller = self.PI(0.2, 0.033, MV, 1)
                controller.send(None)
                # check if the switch needs to be switched
                currAmpSwitch = self.instSwitch.validFrequ(setFrequ)  # check if frequency is valid
                if currAmpSwitch != self.activSwitch:
                    if currAmpSwitch == 1:
                        self.instSwitch.switchAmp1()
                        self.activSwitch = 1
                        print('activeSwitch: %i' % self.activSwitch)
                    elif currAmpSwitch == 2:
                        self.instSwitch.switchAmp2()
                        self.activSwitch = 2
                        print('activeSwitch: %i' % self.activSwitch)
                    elif currAmpSwitch == 3:
                        self.instSwitch.switchAmp3()
                        self.activSwitch = 3
                        print('activeSwitch: %i' % self.activSwitch)
                    elif currAmpSwitch == 4:
                        print('activeSwitch Abort: %i' % self.activSwitch)
                        self.abortTest()
                        break
                self.instSigGen.setFrequMHZ(setFrequ)  # Set Beginning frequency
                self.instSigGen.setAmpDBM(setAPM)  # set beginning amplitude value
                self.instSigGen.switchRFOn()  # set RF ON!!!!!!!!

                self.instSonde.readval()
                currSondeVal = self.instSonde.effEVal
                # Powermeter auslesen eventuell aus bereinigtem Wert
                self.instPowerMeter.switchChannelA()
                self.instPowerMeter.getMeasVal()
                currFwdVal = self.instPowerMeter.currVal
                self.instPowerMeter.switchChannelB()
                self.instPowerMeter.getMeasVal()
                currRevVal = self.instPowerMeter.currVal

                k = 1
                startTime = time.time()
                iRow = 1
                tmpSondeVal = [False] * 3
                while 1:
                    while self.isPaused:
                        time.sleep(0)
                    if self.stopped:
                        break
                    # quadrieren der toleranzen -> kein sqrt nötig
                    if (self.E_T < currSondeVal < self.max_E_L):
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
                            self.abortTest()
                    # Check if Rev and FWD are nearly same
                    if abs(abs(currFwdVal) - abs(currRevVal)) <= self.powMeterTol:
                        print('tolerance fwd and reverse broken with %f' % abs(abs(currFwdVal) - abs(currRevVal)))
                        self.abortTest()
                        break
                    setAPM = MV

                    if abs(abs(prevStepAPM) - abs(setAPM)) > 10:
                        print('APM TO BIG')
                        self.abortTest()

                    self.instSigGen.setAmpDBM(setAPM)
                    self.instSigGen.switchRFOn()  # set RF ON!!!!!!!!!
                    # update measured val
                    timeSonde = time.time()
                    self.instSonde.readval()
                    currSondeVal = self.instSonde.effEVal
                    # print('time sonde:%f' % (time.time()-timeSonde))
                    # print('Updated currSondeVal: %f ' % currSondeVal)
                    t = time.time() - startTime
                    print("currSondeVal %s" % currSondeVal)
                    print("control_E_L %s" % self.control_E_L)
                    MV = controller.send([t, currSondeVal, self.control_E_L])
                    if (k > 5) and ((k % 3) == 0):
                        timePowMetA = time.time()
                        self.instPowerMeter.switchChannelA()
                        self.instPowerMeter.getMeasVal()
                        currFwdVal = self.instPowerMeter.currVal
                        timePowMetB = time.time()
                        self.instPowerMeter.switchChannelB()
                        self.instPowerMeter.getMeasVal()
                        currRevVal = self.instPowerMeter.currVal
                    # print('Updated currRevVal: %f \n' % currRevVal)
                    k = k + 1
                prevStepAPM = setAPM

                # save the values in lists
                self.instPowerMeter.switchChannelA()
                self.instPowerMeter.getMeasVal()
                currFwdVal = self.instPowerMeter.currVal
                self.instPowerMeter.switchChannelB()
                self.instPowerMeter.getMeasVal()
                currRevVal = self.instPowerMeter.currVal
                self.instSonde.readval()
                currSondeVal = self.instSonde.effEVal
                controller.close()
                frequVal.append(setFrequ)
                powFwdVal.append(currFwdVal)
                powRevVal.append(currRevVal)
                sondeListVal.append(currSondeVal)
                powAPMSet.append(setAPM)
                print("1")
                self.countChanged.emit(setFrequ, currFwdVal, currRevVal, currSondeVal, self.position)
                print("2")
                res = [l for l in zip(frequVal, powFwdVal, powRevVal, powAPMSet, sondeListVal)]

                path = 'output_%s_%i.csv' % (self.polarisation, self.position) # abspeichern der csv nach jeder Position
                print("3")
                listCsvFile.append(path)
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for l in res:
                        writer.writerow(l)
                print("3.2")
                self.isWaiting = True  # set isWaiting True to wait change of the position
                print("4")
                # waite for input 'Fortfahren'
            if not self.stopped:
                self.completed = True
                completed = self.completed
                self.completedflag.emit(completed, self.position)
            while self.isWaiting:
                time.sleep(0)
            self.position += 1
    #GUI Fenster öffnet sich mit "Save results?"
        inpPath = 'C:/Users/mlu/Results/calibResult.csv' # Output aus Gui wo ergebnisse abspeichern
        createCalibrationFile(listCsvFile, inpPath)



    def stop(self):
        # print("thread stoped")
        self.stopped = True

    def pause(self):
        self.isPaused = True

    def resum(self):
        self.isPaused = False

    def runNextTest(self):
        self.isWaiting = False


    def abortTest(self):
        self.instSigGen.switchRFOff()
        self.instSwitch.reset()
        print('Test Paused')
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


    def PI(self,Kp, Ki, MV_bar, beta):
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
