# -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
import pyvisa
from WrapperEMRFeldsonde import WrapperEMRFeldsonde
sys.path.append('gui')

class External_FS(QThread):
    countChanged = pyqtSignal(list, int)

# code muss später neu schreiben
    def __init__(self, E_T, f_min, f_max, level, f_step):
        super(External_FS, self).__init__()
        self.E_T = E_T
        self.f_min = f_min
        self.f_max = f_max
        self.Position = Pos
        # self.Polarisation = Polar
        self.Polarisation = Polar
        self.E_L = 1.8 * E_T
        self.signal =1
        self.count = 0
        self.feldsonder = WrapperEMRFeldsonde()

    #def run(self):




    def quit(self):

        print(self.signal)
        #self.gpib_inst.write(':ABOR;*WAI')
        #
        # if (self.signal & 1) == 1:  #是奇数

mess1 = External_FS(1,30, 100, 0, 0)
print(E_T)