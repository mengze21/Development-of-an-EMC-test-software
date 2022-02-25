# -*- coding: utf-8 -*-

import sys
import time
import csv
from csv import reader
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import pyvisa
# Import the Driver for meas Devices
from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator

rm = pyvisa.ResourceManager()
instSonde = WrapperEMRFeldsonde('ASRL3::INSTR', rm)
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR', rm)
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR', rm)
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR', rm)
sys.path.append('gui')


class External_FS_Calib(QThread):
    countChanged = pyqtSignal(list, int)

    def __init__(self, E_T, f_min, f_max, level, f_step, testType, calResultPath, dwellTime):
        super(External_FS_Calib, self).__init__()
        self.testType = testType
        self.calResultPath = calResultPath
        self.dwellTime = dwellTime
        self.E_T = E_T
        self.f_min = f_min
        self.f_max = f_max
        self.f_step = f_step
        self.P_L = level
        self.E_L = 1.8 * self.E_T
        self.startDrive = -30 #Dummy Value
        self.effEval = 30
        self.f_test = self.f_min
        self.instSonde = WrapperEMRFeldsonde('ASRL3::INSTR')
        self.instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR')
        self.instSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
        self.instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR')

    def run(self):
        with open(self.calResultPath, 'r') as read_obj:
            csv_reader = reader(read_obj)
            listCalFile = list(csv_reader)
            print(listCalFile)
        activSwitch = 0
        # Signal generator level calibration
        if self.testType == '1':
            # 0 = Frequency
            # 1 = Forward Power
            # 2 = Reverse Power
            # 3 = Power Signal Generator
            # 4 = Electric Field Strength
            # 5 = Cal Success Status
            k = 1
            for x in listCalFile:
                while self.isPaused:
                    time.sleep(0)
                if self.stopped:
                    break
                setFrequ = float(x[0])
                setAPM = float(x[3])
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
                        self.abortTest()
                        break
                instSigGen.setFrequMHZ(setFrequ)  # Set Frequency
                instSigGen.setAmpDBM(setAPM)  # set amplitude value from Cal File
                instSigGen.switchRFOn()  # set RF ON!!!!!!!
                currSondeVal = instSonde.readval()
                instSigGen.switchAPModulationON()
                time.sleep(self.dwellTime)
                k = k + 1
                instSigGen.switchAPModulationOFF()
                #self.countChanged.emit(setFrequ, currSondeVal)

            if not self.stopped:
                self.completed = True
                completed = self.completed
                self.completedflag.emit(completed, self.position)





        # Forward Power Calibration
        elif self.testType == '2':
            fwdTol = 0.1

            j = 1
            powFwdVal = []
            for x in listCalFile:
                while self.isPaused:
                    time.sleep(0)
                if self.stopped:
                    break
                setFrequ = float(x[0])
                setFwdPow = float(x[1])
                MV = float(x[3])
                controller = self.PI(0.3, 0.22, MV, 1)
                controller.send(None)
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
                        self.abortTest()
                        break
                instSigGen.setFrequMHZ(setFrequ)  # Set Frequency
                instSigGen.setAmpDBM(MV)  # set amplitude value from Cal File
                instSigGen.switchRFOn()  # set RF ON!!!!!!!!
                startTime = time.time()
                instPowerMeter.switchChannelA()
                instPowerMeter.getMeasVal()
                currFwdVal = instPowerMeter.currVal
                k = 1
                # print('Goal Fwd Value: %f' % setFwdPow)
                iRow = 1
                tmpFwdVal = [False] * 4
                while 1:
                    while self.isPaused:
                        time.sleep(0)
                    if self.stopped:
                        break
                    if (setFwdPow < currFwdVal < setFwdPow + fwdTol):
                        tmpFwdVal[iRow] = True
                    else:
                        tmpFwdVal[iRow] = False

                    # print(tmpFwdVal)
                    iRow = iRow + 1
                    if iRow > 3:
                        iRow = 0

                    if all(tmpFwdVal):
                        break

                    instSigGen.setAmpDBM(MV)
                    instPowerMeter.getMeasVal()
                    currFwdVal = instPowerMeter.currVal
                    # print('Current Fwd Value: %f' % currFwdVal)
                    t = time.time() - startTime
                    MV = controller.send([t, currFwdVal, setFwdPow + 0.05])
                    # print('Control MV Value: %f' % MV)
                    k = k + 1
                instSonde.readval()
                instSigGen.switchAPModulationON()
                time.sleep(self.dwellTime)
                print('T', instSonde.effEVal)
                j = j + 1
                instSigGen.switchAPModulationOFF()
                controller.close()
                powFwdVal.append(currFwdVal)
                #self.countChanged.emit(setFrequ, currSondeVal)
            if not self.stopped:
                self.completed = True
                completed = self.completed
                self.completedflag.emit(completed, self.position)





        # self.instSigGen.setFrequMHZ(self.f_min)
        # self.instSigGen.setAmpDBM(self.startDrive)

        # self.activeSwitch = self.instSwitch.validFrequ(self.f_min)
        # if self.activeSwitch == 1:
        #     self.instSwitch.switchAmp1()
        # elif self.activeSwitch == 2:
        #     self.instSwitch.switchAmp2()
        # elif self.activeSwitch == 3:
        #     self.instSwitch.switchAmp3()
        # else:
        #     raise ValueError('Frequency not possible with current amplifier!')

        # while self.f_test < self.f_max:
        #     #self.sonde.readval()
        #     #while self.E_L < self.sonde.effEVal:
        #         #self.P_L = self.P_L + 1         # P_L step level?
        #     #self.effEval = 30
        #     #if self.effEval < self.E_L:
        #         #readval(self)
        #         #self.P_L += 5
        #     self.f_test = self.f_test + self.f_step * self.f_test
        #     #print(self.E_L)
        #     #print(self.E_T)
        #     print(self.f_test)



    def abortTest(self):
        instSigGen.switchRFOff()
        instSwitch.reset()
        print('Test Paused')
        sys.exit()


    def checkValues(self, gridValFrequ, gridValFwd):
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

    def stop(self):
        # print("thread stoped")
        self.stopped = True

    def pause(self):
        self.isPaused = True

    def resum(self):
        self.isPaused = False


