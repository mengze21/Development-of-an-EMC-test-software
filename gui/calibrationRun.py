# Import the Driver for meas Devices
import sys
import time
from typing import List

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator

sys.path.append('gui')
# start Values
startFrequ = 80
endFrequ = 1000
frequStep = 1.01
polarisation = 'vertical'
E_T = 18  # Prüffeldstärke
E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
E_L_Tol = 0.1
min_E_L = E_L - E_L_Tol
max_E_L = E_L + E_L_Tol
totalPoints = 5
startAPM = -30
stepAPM = 0.5
maxAPMPoss = 10
powMeterTol = 5
activSwitch = 0

# Driver selection
instSonde = WrapperEMRFeldsonde('ASRL3::INSTR')
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR')
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR')
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR')
setFrequ = startFrequ
setAPM = startAPM

# list creation
frequVal = []
powFwdVal = []
gridValFrequ = []
gridValFwd = []

def abortTest():
    instSigGen.switchRFOff()
    instSwitch.reset()
    print('Test Aborted')

def checkValues(gridValFrequ, gridValFwd):
    isvalid = []
    crntDbms = []
    cntFrequ = len(gridValFwd[1])
    for iFrequ in range(cntFrequ):
        maxDiff = 0
        crntDbms.clear()
        for i in range(len(gridValFwd)):
            crntDbms.append(gridValFwd[i][iFrequ])
        minVal = min(crntDbms)
        maxVal = max(crntDbms)
        maxDiff = abs(minVal-maxVal)
        if maxDiff > 6:
            isvalid.append(0)
        else:
            isvalid.append(1)

for currPoint in range(1, totalPoints + 1, 1):
    flgGridPoint = input('Feldsonde aufgestellt?: \n')
    if flgGridPoint == 'yes':
        currAmpSwitch = instSwitch.validFrequ(setFrequ) # check if frequency is valid
        if currAmpSwitch == 1:
            instSwitch.switchAmp1()
            activSwitch = 1
        elif currAmpSwitch == 2:
            instSwitch.switchAmp2()
            activSwitch = 2
        elif currAmpSwitch == 3:
            instSwitch.switchAmp3()
            activSwitch = 3
        elif currAmpSwitch == 4:
            break

        instSigGen.setFrequMHZ(setFrequ) # Set Beginning frequency
        instSigGen.setAmpDBM(setAPM) # set beginning amplitude value
        instSigGen.switchRFOn() # set RF ON!!!!!!!!!

        currSondeVal = instSonde.readval()
        instPowerMeter.switchChannelA()
        currFwdVal = instPowerMeter.getMeasVal()
        instPowerMeter.switchChannelB()
        currRevVal = instPowerMeter.getMeasVal()
        while setFrequ <= endFrequ:

            # check if the switch needs to be switched
            currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
            if currAmpSwitch != activSwitch:
                if currAmpSwitch == 1:
                    instSwitch.switchAmp1()
                    activSwitch = 1
                elif currAmpSwitch == 2:
                    instSwitch.switchAmp2()
                    activSwitch = 2
                elif currAmpSwitch == 3:
                    instSwitch.switchAmp3()
                    activSwitch = 3
                elif currAmpSwitch == 4:
                    abortTest()
                    break

            # Now do the loop to find the correct E_L Value
            while min_E_L < currSondeVal < max_E_L:
            # Check if Rev and FWD are nearly same
                if abs(abs(currFwdVal)-abs(currRevVal)) <= powMeterTol:
                    abortTest()
                    break
                if currSondeVal < max_E_L:
                    setAPM = setAPM + stepAPM
                else:
                    setAPM = setAPM - stepAPM
                instSigGen.setAmpDBM(setAPM)

                time.sleep(3)

                # update Measured Values
                instPowerMeter.switchChannelA()
                currFwdVal = instPowerMeter.getMeasVal()
                instPowerMeter.switchChannelB()
                currRevVal = instPowerMeter.getMeasVal()
                currSondeVal = instSonde.readval()

            # save the values in lists
            frequVal.append(setFrequ)
            powFwdVal.append(currFwdVal)
            setFrequ = setFrequ * frequStep

    else:
        break
    gridValFrequ.append(frequVal)
    gridValFwd.append(powFwdVal)