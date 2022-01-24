from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperSignalGenerator import WrapperSignalGenerator
from WrapperPowerMeter import WrapperPowerMeter
import time



instWrapperEMR = WrapperEMRFeldsonde("ASRL3::INSTR") # Adresse als Variable von GUI übernehmen
instWrapperSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
instWrapperSwitch.reset()

instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR')
time.sleep(10)

instWrapperSwitch.switchAmp1()
# time.sleep(10)
# instWrapperSwitch.switchAmp2()
# # time.sleep(10)
# instWrapperSwitch.switchAmp3()
# time.sleep(10)

instPowerMet = WrapperPowerMeter('GPIB0::11::INSTR')
time.sleep(2)
instSigGen.switchRFOn()

while 1:
    revCh = input("Enter Channel:  \n")
    if revCh == 'B':
        instPowerMet.switchChannelB()
        print('Switch Channel to B')
    else:
        instPowerMet.switchChannelA()
        print('Switch Channel to A')
    instPowerMet.getMeasVal()
    print(instPowerMet.currVal)
    instWrapperEMR.readval()
    instPowerMet.getMeasVal()
    print(instPowerMet.currVal)
    instWrapperEMR.readval()
    instPowerMet.getMeasVal()
    print(instPowerMet.currVal)
    instWrapperEMR.readval()
    flgAbort = input("Abort Meas?  \n")
    if flgAbort == 'yes':
        break
    newVal = input("Enter AMP:  \n")
    instSigGen.setAmpDBM(float(newVal))


instWrapperSwitch.reset()
instSigGen.setAmpDBM(-100)
instSigGen.switchRFOff()




