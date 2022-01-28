import sys
sys.path.append('gui')
import pyvisa
import time
import re
from math import sqrt

class WrapperEMRFeldsonde:
    def __init__(self,address, resourceManager):
     self.address = address
     self.rm = resourceManager
     self.emrInst = self.rm.open_resource(self.address)
     self.emrInst.baud_rate = 4800
     self.emrInst.timeout = 10000
     self.emrInst.query_delay = 0.1
     self.emrInst.read_termination = '\n'
     self.emrInst.write_termination = '\n'
     self.emrInst.write('SYST:BEEP')
     time.sleep(1)
     self.emrInst.write('SYST:BEEP')

# read the val as vectors and eff Val or peak val
    def readval(self):
        self.currVal = self.emrInst.query('MEAS?');
        self.listVal = re.findall("[0-9]{1,5}[.][0-9]{2}",  self.currVal)
        self.Ex = float(self.listVal[0])
        self.Ey = float(self.listVal[1])
        self.Ez = float(self.listVal[2])
        self.effEVal = sqrt(pow(self.Ex,2)+pow(self.Ey,2)+pow(self.Ez,2))
        #print('Ex:' , self.Ex)
        #print('Ey:' , self.Ey)
        #print('Ez:' , self.Ez)