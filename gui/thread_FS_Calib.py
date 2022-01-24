# -*- coding: utf-8 -*-

import sys
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import pyvisa
# Import the Driver for meas Devices
from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
sys.path.append('gui')



class External_FS_Calib(QThread):
    countChanged = pyqtSignal(list, int)

    def __init__(self, E_T, f_min, f_max, level, f_step):
        super(External_FS_Calib, self).__init__()
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
        # currPowMetValA = self.instPowerMeter.getMeasVal()
        # currPowMetValB = self.instPowerMeter.getMeasVal()
        # print('PowMeterValue A: %f' % currPowMetValA)
        # print('PowMeterValue B: %f' % currPowMetValB)
        print('T')
        time.sleep(10)
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


    def quit(self):
        pass





