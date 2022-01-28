import pyvisa

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperSignalGenerator import WrapperSignalGenerator
from WrapperPowerMeter import WrapperPowerMeter
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

rm = pyvisa.ResourceManager()
instWrapperEMR = WrapperEMRFeldsonde("ASRL3::INSTR", rm) # Adresse als Variable von GUI übernehmen
# instWrapperEMR.readval()
# print(instWrapperEMR.currVal)
# instWrapperSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
# instWrapperSwitch.reset()

# instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR')
# time.sleep(10)

# instWrapperSwitch.switchAmp1()
# instWrapperSwitch.switchAmp2()
# instWrapperSwitch.switchAmp3()
# time.sleep(10)
while 1:
    startTime = time.time()
    instWrapperEMR.readval()
    currSondeVal = instWrapperEMR.currVal
    print(time.time()-startTime)

# instPowerMet = WrapperPowerMeter('GPIB0::11::INSTR')
# instSigGen.switchRFOn()
# startTime = time.time()

#     print(time.time()-startTime)
#     # print(instPowerMet.currVal)
#     flgAbort = input("Abort Meas?  \n")
#     if flgAbort == 'yes':
#         break

