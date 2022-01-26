# Import the Driver for meas Devices
import sys
from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator

sys.path.append('gui')
startFrequ = 80
endFrequ = 1000
frequStep = 0.01
polarisation = 'vertical'
E_T = 18  # Prüffeldstärke
E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
totalPoints = 5
startAPM = -30

instSonde = WrapperEMRFeldsonde('ASRL3::INSTR')
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR')
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR')
setFrequ = startFrequ
for currPoint in range(1, totalPoints + 1, 1):
    flgGridPoint = input('Feldsonde aufgestellt?: \n')
    if flgGridPoint == 'yes':
        currAmpSwitch = instSwitch.validFrequ(setFrequ) # check if frequency is valid
        if currAmpSwitch == 1:
            instSwitch.switchAmp1()
        elif currAmpSwitch == 2:
            instSwitch.switchAmp2()
        elif currAmpSwitch == 3:
            instSwitch.switchAmp3()
        elif currAmpSwitch == 4:
            break
    else:
        break