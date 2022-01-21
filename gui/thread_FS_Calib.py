# -*- coding: utf-8 -*-

import sys
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import pyvisa
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
        self.effEval = 30
        self.f_test = self.f_min
        #self.sonde = WrapperEMRFeldsonde('GPIB0::21::INSTR')

    def run(self):
        print(self.f_test)
        #self.sonde.address = 'GPIB0::21::INSTR'
       # self.sonde.rm = pyvisa.ResourceManager()
        #self.sonde.emrInst = self.rm.open_resource(self.address)
        #self.sonde.emrInst.baud_rate = 4800
        #self.sonde.emrInst.timeout = 10000
        #self.sonde.emrInst.query_delay = 0.1
        #self.sonde.emrInst.read_termination = '\n'
        #self.sonde.emrInst.write_termination = '\n'
        #self.sonde.emrInst.write('SYST:BEEP')
        #time.sleep(1)
        #self.sonde.emrInst.write('SYST:BEEP')

        while self.f_test < self.f_max:
            #self.sonde.readval()
            #while self.E_L < self.sonde.effEVal:
                #self.P_L = self.P_L + 1         # P_L step level?
            #self.effEval = 30
            #if self.effEval < self.E_L:
                #readval(self)
                #self.P_L += 5
            self.f_test = self.f_test + self.f_step * self.f_test
            #print(self.E_L)
            #print(self.E_T)
            print(self.f_test)






