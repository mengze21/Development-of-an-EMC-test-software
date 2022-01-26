import sys
sys.path.append('gui')
import pyvisa
import time
import re
import numpy

class WrapperPowerMeter:
    def __init__(self,address):
        self.address = address
        self.rm = pyvisa.ResourceManager()
        self.sigPowerMeterInst = self.rm.open_resource(self.address)
        self.sigPowerMeterInst.read_termination = '\n'
        self.sigPowerMeterInst.write_termination = '\n'
        self.sigPowerMeterInst.timeout = 10000
        self.sigPowerMeterInst.query_delay = 0.1
        self.sigPowerMeterInst.write('*RCL 0')
        self.setFilterLevel(5)
        self.setDispOff()
        self.setUnitDBM()
        self.getMeasVal()

    def switchChannelA(self):
        self.sigPowerMeterInst.write('INP:SEL "A"')
        self.setUnitDBM()
        self.setFilterLevel(5)
        time.sleep(1)


    def switchChannelB(self):
        self.sigPowerMeterInst.write('INP:SEL "B"')
        self.setUnitDBM()
        self.setFilterLevel(5)
        time.sleep(1)

    def setFilterLevel(self,val):
        self.sigPowerMeterInst.write('CALC:FILT:NSEL %d' % val)

    def setUnitDBM(self):
        self.sigPowerMeterInst.write('POW:UNIT DBM')

    def getMeasVal(self):
        self.currVal = self.sigPowerMeterInst.query('*TRG')

    def setDispOff(self):
        self.sigPowerMeterInst.write(':DISP:ENAB OFF')
