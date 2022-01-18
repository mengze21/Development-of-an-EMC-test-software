from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
import time
import cProfile

#instWrapperEMR = WrapperEMRFeldsonde("ASRL3::INSTR") # Adresse als Variable von GUI übernehmen
#instWrapperEMR.readval()
instWrapperSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
time.sleep(2)
instWrapperSwitch.switchAmp1()
time.sleep(10)
instWrapperSwitch.switchAmp2()
time.sleep(10)
instWrapperSwitch.switchAmp3()
time.sleep(10)
instWrapperSwitch.reset()