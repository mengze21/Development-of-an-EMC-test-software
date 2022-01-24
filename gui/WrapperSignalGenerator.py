import sys
sys.path.append('gui')
import pyvisa
import time
import re
import numpy

class WrapperSignalGenerator:
    def __init__(self,address):
     self.address = address
     self.rm = pyvisa.ResourceManager()
     self.sigGenInst = self.rm.open_resource(self.address)
     self.sigGenInst.read_termination = '\n'
     self.sigGenInst.write_termination = '\n'
     self.sigGenInst.timeout = 10000
     self.sigGenInst.query_delay = 0.1
     self.setFrequMHZ(80.0)
     self.setAmpDBM(-30)
     self.switchAPModulationOFF()
     self.switchRFOff()
     time.sleep(1)

    def switchRFOn(self):
      self.sigGenInst.write('R3')

    def switchRFOff(self):
      self.sigGenInst.write('R2')

    def setFrequMHZ(self, val):
      self.sigGenInst.write('FR %f MZ' % val)

    def setAmpDBM(self, val):
      self.sigGenInst.write('AP %f DM' % val)

    def switchAPModulationOFF(self):
      self.sigGenInst.write('AM S1 S4')
      time.sleep(1)
      self.sigGenInst.write('AM S2 S4')
      time.sleep(1)
      self.sigGenInst.write('AM S3 S4')
