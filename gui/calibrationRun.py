# Import the Driver for meas Devices
import sys
import csv

from typing import List
import pyvisa

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator

from tqdm import tqdm
#plot stuiff
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import time

sys.path.append('gui')
# start Values
startFrequ = 80
endFrequ = 1000
frequStep = 1.01
polarisation = 'vertical'
E_T = 3 # Prüffeldstärke
E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
E_L_Tol = 0.6
max_E_L = E_L + E_L_Tol
control_E_L = E_L + E_L_Tol/2
totalPoints = 5
startAPM = -27
stepAPM = 0
# maxAPMPoss = -10
powMeterTol = 0.5
activSwitch = 0
maxChangeVal = 10
prevStepAPM = startAPM

# Driver selection
rm = pyvisa.ResourceManager()
instSonde = WrapperEMRFeldsonde('ASRL3::INSTR', rm)
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR', rm)
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR', rm)
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR', rm)
setFrequ = startFrequ
setAPM = startAPM

# list creation
frequVal = []
powFwdVal = []
sondeListVal = []
gridValFrequ = []
gridValFwd = []
powRevVal = []
powAPMSet  = []

def abortTest():
    instSigGen.switchRFOff()
    instSwitch.reset()
    print('Test Aborted')
    sys.exit()

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


def PI(Kp, Ki, MV_bar, beta):
    # initialize stored data
    t_prev = -1
    I = 0

    # initial control
    MV = MV_bar

    while True:
        # yield MV, wait for new t, SP, PV
        t, PV, SP = yield MV

        # PI calculations
        P = Kp * (beta * SP - PV)
        I = I + Ki * (SP - PV) * (t - t_prev)
        # print('P: %f' % P)
        # print('I: %f' % I)
        MV = MV_bar + P + I

        # print('New MV: %f' % MV)
        # update stored data for next iteration
        t_prev = t



ii = 1
for currPoint in range(2, totalPoints + 1, 1):

    frequVal.clear()
    powFwdVal.clear()
    powRevVal.clear()
    sondeListVal.clear()
    setFrequ = startFrequ
    setAPM = startAPM
    flgGridPoint = input('Feldsonde aufgestellt?: \n')
    if flgGridPoint == 'yes':
        currAmpSwitch = instSwitch.validFrequ(setFrequ) # check if frequency is valid
        if currAmpSwitch == 1:
            instSwitch.switchAmp1()
            activSwitch = 1
            print('activeSwitch: %i ' % activSwitch)
        elif currAmpSwitch == 2:
            instSwitch.switchAmp2()
            activSwitch = 2
            print('activeSwitch: %i' % activSwitch)
        elif currAmpSwitch == 3:
            instSwitch.switchAmp3()
            activSwitch = 3
            print('activeSwitch: %i ' % activSwitch)
        elif currAmpSwitch == 4:
            print('activeSwitch Abort: %i ' % activSwitch)
            break

        frequList = []
        while setFrequ <= endFrequ:
            frequList.append(setFrequ)
            setFrequ = setFrequ * 1.01

        for i in tqdm(frequList, desc ="Calibration Frequ Step:"):
            setFrequ = i
            plt.ion()  ## Note this correction
            fig = plt.figure()
            plt.title("constant field strength control")
            plt.xlabel("Step")
            plt.ylabel("field strength")
            plt.axis([0, 60, 2, 9])
            plt.axhline(y=control_E_L, color='b', linestyle='-')
            plt.axhline(y=max_E_L, color='r', linestyle='-')
            plt.axhline(y=E_L, color='g', linestyle='-')

            MV = setAPM
            # print('SetFrequ: %f' % setFrequ)
            instSigGen.switchRFOff() # set RF ON!!!!!!!!!
            controller = PI(0.2, 0.033, MV, 1)
            controller.send(None)
            # time.sleep(20)
            # check if the switch needs to be switched
            currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
            # print('Needed Amplfiier: %i' % currAmpSwitch)
            if currAmpSwitch != activSwitch:
                if currAmpSwitch == 1:
                    instSwitch.switchAmp1()
                    activSwitch = 1
                    print('activeSwitch: %i' % activSwitch)
                elif currAmpSwitch == 2:
                    instSwitch.switchAmp2()
                    activSwitch = 2
                    print('activeSwitch: %i' % activSwitch)
                elif currAmpSwitch == 3:
                    instSwitch.switchAmp3()
                    activSwitch = 3
                    print('activeSwitch: %i' % activSwitch)
                elif currAmpSwitch == 4:
                    print('activeSwitch Abort: %i' % activSwitch)
                    abortTest()
                    break
            instSigGen.setFrequMHZ(setFrequ)  # Set Beginning frequency
            # if setAPM > maxAPMPoss:
            #     abortTest()
            instSigGen.setAmpDBM(setAPM)  # set beginning amplitude value
            instSigGen.switchRFOn()  # set RF ON!!!!!!!!


            instSonde.readval()
            currSondeVal = instSonde.effEVal
            instPowerMeter.switchChannelA()
            instPowerMeter.getMeasVal()
            currFwdVal = instPowerMeter.currVal
            instPowerMeter.switchChannelB()
            instPowerMeter.getMeasVal()
            currRevVal = instPowerMeter.currVal


            # Now do the loop to find the correct E_L Value
            # print('currSondeVal: %f' % currSondeVal)
            # print('CurrFwdVal: %f' % currFwdVal)
            # print('currRevVal: %f' % currRevVal)
            k = 1
            startTime = time.time()
            iRow = 1
            tmpSondeVal = [False]*3
            while 1:
                # quadrieren der toleranzen -> kein sqrt nötig
                if (E_L < currSondeVal < max_E_L):
                    # find at least 3 Sondeval in Row to validate
                    tmpSondeVal[iRow] = True
                else:
                    tmpSondeVal[iRow] = False

                # print(tmpSondeVal)
                iRow = iRow + 1
                if iRow > 2:
                    iRow = 0

                if all(tmpSondeVal):
                    break

                if (k % 60) == 0:
                    continueTest = input('Continue Test?\n')
                    if continueTest == 'No':
                        abortTest()
            # Check if Rev and FWD are nearly same
                if abs(abs(currFwdVal)-abs(currRevVal)) <= powMeterTol:
                    print('tolerance fwd and reverse broken with %f' % abs(abs(currFwdVal)-abs(currRevVal)))
                    abortTest()
                    break
                # if currSondeVal < max_E_L:
                #     setAPM = setAPM + stepAPM
                # else:
                #     setAPM = setAPM - stepAPM
                # print('updated APMval: %f \n' % setAPM)

                # if setAPM > maxAPMPoss:
                #     abortTest()

                # piyes = input('set MV TO APM?')
                # if piyes == 'yes':
                #     print('set APM to %f' % MV)
                # print('set APM to %f' % MV)
                setAPM = MV

                if abs(abs(prevStepAPM) - abs(setAPM)) > maxChangeVal:
                    print('APM TO BIG')
                    abortTest()

                instSigGen.setAmpDBM(setAPM)
                instSigGen.switchRFOn()  # set RF ON!!!!!!!!!
                #update measured val
                timeSonde = time.time()
                instSonde.readval()
                currSondeVal = instSonde.effEVal
                # print('time sonde:%f' % (time.time()-timeSonde))
                # print('Updated currSondeVal: %f ' % currSondeVal)
                t = time.time()-startTime
                MV = controller.send([t, currSondeVal, control_E_L])
                if (k > 5) and ((k % 3) == 0):
                    timePowMetA = time.time()
                    instPowerMeter.switchChannelA()
                    instPowerMeter.getMeasVal()
                    currFwdVal = instPowerMeter.currVal
                    #print('time PowerMeterA:%f' % (time.time()-timePowMetA))
                    # print('Updated CurrFwdVal: %f \n' % currFwdVal)
                    timePowMetB = time.time()
                    instPowerMeter.switchChannelB()
                    instPowerMeter.getMeasVal()
                    currRevVal = instPowerMeter.currVal
                    #print('time PowerMeterB:%f' % (time.time()-timePowMetB))
                # print('Updated currRevVal: %f \n' % currRevVal)
                k = k + 1
                plt.scatter(k, currSondeVal)
                plt.show()
                plt.pause(0.001)
            prevStepAPM = setAPM


            # save the values in lists

            instPowerMeter.switchChannelA()
            instPowerMeter.getMeasVal()
            currFwdVal = instPowerMeter.currVal
            instPowerMeter.switchChannelB()
            instPowerMeter.getMeasVal()
            currRevVal = instPowerMeter.currVal
            instSonde.readval()
            currSondeVal = instSonde.effEVal
            controller.close()
            frequVal.append(setFrequ)
            powFwdVal.append(currFwdVal)
            powRevVal.append(currRevVal)
            sondeListVal.append(currSondeVal)
            powAPMSet.append(setAPM)
            plt.savefig('graphs/Field_strength_%s_%i_%i' % (polarisation, currPoint, ii))
            plt.close()
            # print('Saved currFwdVal: %f' % currFwdVal)
            res = [l for l in zip(frequVal, powFwdVal, powRevVal, powAPMSet, sondeListVal)]
            path = 'output_%s_%i.csv' % (polarisation, currPoint)
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for l in res:
                    writer.writerow(l)
            ii = ii + 1
    else:
        break

    gridValFrequ.append(frequVal)
    gridValFwd.append(powFwdVal)