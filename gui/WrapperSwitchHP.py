import sys
sys.path.append('gui')
import pyvisa
import time
import re
import numpy

class WrapperSwitchHP:
    def __init__(self,address):
     self.address = address
     self.currAmplifier = 0
     self.rm = pyvisa.ResourceManager()
     self.switchInst = self.rm.open_resource(self.address)
     self.switchInst.timeout = 10000
     self.switchInst.query_delay = 0.1
     self.switchInst.read_termination = '\n'
     self.switchInst.write_termination = '\n'
     self.switchInst.write('DISP ready')


# read the val as vectors and eff Val or peak val
    def reset(self):
        self.switchInst.write('RESET')
        succList = [False, False, False]
        for i in range(1, 4):
            inpBuffer = "VIEW 10"+str(i)
            ansBuffer = self.switchInst.query(inpBuffer)
            if ansBuffer[0:4] == "OPEN":
                succList[i-1] = True
            time.sleep(0.8)
        if succList and all(elem for elem in succList):
            self.switchInst.write('DISP reset success')
            return True
        self.switchInst.write('DISP reset Failed')
        return False
        print(succList)
# so the only slot that is used is one. and they are closed in channel 1, 2, 3
# always do a reset before every command and check if every channel is open to guarantee nothing fails, since multiple relais can be closed
# CLOSE 101 and 102, 103 are open ====> uses amplifier 1! CHECK FOR RESET BEFORE
# CLOSE 102 and 101, 103 are open ====> uses amplifier 2! CHECK FOR RESET BEFORE
# CLOSE 103 and 101, 102 are open ====> uses amplifier 3! CHECK FOR RESET BEFORE

    def switchAmp1(self):
        # Reset before doing anything!
        if self.reset():
            self.switchInst.write('CLOSE 101')
            self.switchInst.write('DISP AMP1 active')
            return True
        return False

    def switchAmp2(self):
        # Reset before doing anything!
        if self.reset():
            self.switchInst.write('CLOSE 102')
            self.switchInst.write('DISP AMP2 active')
            return True
        return False

    def switchAmp3(self):
        # Reset before doing anything!
        if self.reset():
            self.switchInst.write('CLOSE 103')
            self.switchInst.write('DISP AMP3 active')
            return True
        return False
