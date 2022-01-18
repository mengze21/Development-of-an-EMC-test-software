# -*- coding: utf-8 -*-

import sys
sys.path.append('gui')
import time
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import math
import pyvisa

class External_LS(QThread):
    countChanged = pyqtSignal(float, float, float)
    def __init__(self, AnfangF,frequenz_S,Spannung,frequenz_L,Leistung):
        super(External_LS, self).__init__()
        self.Anfangsfrequency = AnfangF
        self.frequenz_S= frequenz_S
        self.Spannung=Spannung
        self.frequenz_L=frequenz_L
        self.Leistung=Leistung
        self.signal = 1

        # read the addresse of the instrument
        self.rm = pyvisa.ResourceManager()
        self.gpib_addr2 = 'GPIB0::21::INSTR'
        self.gpib_addr3 = 'GPIB0::9::INSTR'
        self.SignalGenerator = self.rm.open_resource(self.gpib_addr2)
        self.HpSwitch = self.rm.open_resource(self.gpib_addr3)
        # Settings for signalgenerator
        self.SignalGenerator.write('AM S1 S4')
        self.SignalGenerator.write('AM S2 S4')
        self.SignalGenerator.write('AM S3 S4')
        self.SignalGenerator.write('FR 1 MZ')
        self.SignalGenerator.write('R3')
        self.SignalGenerator.write('FR 0.15 MZ')
        # Settings for Switch Unit (just use one) to open the amplifier
        self.HpSwitch.write('OLAP 0')
        self.HpSwitch.write('CLOSE 101')
        self.HpSwitch.write('CMON 1')

    def run(self):

        # used to update the diagram
        print(self.frequenz_L)
        print(self.Leistung)
        print(self.frequenz_S)
        print(self.Spannung)

        for a, b in zip(self.frequenz_L, self.Leistung):
            if a >= self.Anfangsfrequency:
                if (self.signal & 1) == 1:
                    Sollspannung = np.interp(a, self.frequenz_S, self.Spannung)
                    PdBm1 = 33
                    PdBm3 = 33 * math.log10(20 * Sollspannung ** 2) / (math.log10(20 * 10 ** 2))
                    leistung_real = b + PdBm3 - PdBm1
                    FR = a
                    AP = leistung_real
                    # signalgenerator emits a specific amount of power at a specific frequency
                    self.SignalGenerator.write('FR %s MZ' % str(FR))
                    self.SignalGenerator.write('AP %s DM' % str(AP))
                    self.countChanged.emit(a, leistung_real,Sollspannung)  # Transfer of real-time data to TestWindow_LS, presented in a window therein.
                    self.Anfangsfrequency = a
                    time.sleep(0.2)

        self.SignalGenerator.write('AP -50 DM')
        self.SignalGenerator.write('R2')
        # close the amplifier
        self.HpSwitch.write('OLAP 0')
        self.HpSwitch.write('OPEN 101')
        self.HpSwitch.write('CMON 1')