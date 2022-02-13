# Import the Driver for meas Devices
import sys
import csv
from csv import reader


from typing import List
import pyvisa

from WrapperEMRFeldsonde import WrapperEMRFeldsonde
from WrapperSwitchHP import WrapperSwitchHP
from WrapperPowerMeter import WrapperPowerMeter
from WrapperSignalGenerator import WrapperSignalGenerator
#plot stuiff

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import time

sys.path.append('gui')

# start Values
polarisation = 'vertical'
activSwitch = 0
maxStayTime = 1

# Driver selection
rm = pyvisa.ResourceManager()
instPowerMeter = WrapperPowerMeter('GPIB0::11::INSTR', rm)
instSwitch = WrapperSwitchHP('GPIB0::9::INSTR', rm)
instSigGen = WrapperSignalGenerator('GPIB0::21::INSTR', rm)

# list creation
powFwdVal = []
powRevVal = []

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
        print('P: %f' % P)
        print('I: %f' % I)
        MV = MV_bar + P + I

        print('New MV: %f' % MV)
        # update stored data for next iteration
        t_prev = t




# Read the csv file as rows in the list.
# Format is the following frequency, Forward Power , Reverse Power, Power for the SignalGenerator, Electric Field Strength.
with open('output.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    listCalFile = list(csv_reader)
    print(listCalFile)


testType = input('Welche Testart?: \n')

# Signal generator level calibration
if testType == '1':
    print('1 selected')
    rowSize = len(listCalFile)
    print(rowSize)
    print(listCalFile[rowSize-1][0])
    # 0 = Frequency
    # 1 = Forward Power
    # 2 = Reverse Power
    # 3 = Power Signal Generator
    # 4 = Electric Field Strength

    for x in listCalFile:
        setFrequ = x[0]
        setAPM = x[3]
        currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
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

        instSigGen.setFrequMHZ(setFrequ)  # Set Frequency
        instSigGen.setAmpDBM(setAPM) # set amplitude value from Cal File
        instSigGen.switchRFOn()  # set RF ON!!!!!!!!
        time.sleep(maxStayTime)


# Forward Power Calibration
elif testType == '2':
    fwdTol = 0.2
    print('2 selected')
    for x in listCalFile:
        setFrequ = float(x[0])
        setFwdPow = float(x[1])
        MV = float(x[3])
        print(setFrequ)
        print(setFwdPow)
        print(MV)
        plt.ion()  ## Note this correction
        fig = plt.figure()
        plt.title("Forward Power Control")
        plt.xlabel("Step")
        plt.ylabel("Forward Power")
        plt.axis([0, 100, -23, -10])
        plt.axhline(y=(setFwdPow + fwdTol), color='r', linestyle='-')
        controller = PI(0.3, 0.22, MV, 1)
        controller.send(None)
        currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
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
        instSigGen.setFrequMHZ(setFrequ)  # Set Frequency
        instSigGen.setAmpDBM(MV)  # set amplitude value from Cal File
        instSigGen.switchRFOn()  # set RF ON!!!!!!!!
        startTime = time.time()
        instPowerMeter.switchChannelA()
        instPowerMeter.getMeasVal()
        currFwdVal = instPowerMeter.currVal
        k = 1
        print('Goal Fwd Value: %f' % setFwdPow)
        iRow = 1
        tmpFwdVal = [False] * 4
        while 1:
            if (setFwdPow < currFwdVal < setFwdPow + fwdTol ):
                tmpFwdVal[iRow] = True
            else:
                tmpFwdVal[iRow] = False

            print(tmpFwdVal)
            iRow = iRow + 1
            if iRow > 3:
                iRow = 0

            if all(tmpFwdVal):
                break

            instSigGen.setAmpDBM(MV)
            instPowerMeter.getMeasVal()
            currFwdVal = instPowerMeter.currVal
            print('Current Fwd Value: %f' % currFwdVal)
            t = time.time() - startTime
            MV = controller.send([t, currFwdVal, setFwdPow + fwdTol])
            print('Control MV Value: %f' % MV)
            k = k + 1
            plt.scatter(k, currFwdVal)
            plt.show()
            plt.pause(0.001)

        controller.close()
        powFwdVal.append(currFwdVal)
        plt.close()



elif testType == '3':
    print('3 selected')
    netPowTol = 0.3
    for x in listCalFile:
        setFrequ = float(x[0])
        FwdPow = float(x[1])
        RevPow = float(x[2])
        MV = float(x[3])
        print(setFrequ)
        print(FwdPow)
        print(RevPow)
        print(MV)
        setNetPower = FwdPow - RevPow
        plt.ion()  ## Note this correction
        fig = plt.figure()
        plt.title("Net Power Control")
        plt.xlabel("Step")
        plt.ylabel("Net Power")
        plt.axis([0, 100, -5, 12])
        plt.axhline(y=(setNetPower + netPowTol), color='r', linestyle='-')
        controller = PI(0.3, 0.22, MV, 1)
        controller.send(None)
        currAmpSwitch = instSwitch.validFrequ(setFrequ)  # check if frequency is valid
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

        instSigGen.setFrequMHZ(setFrequ)  # Set Frequency
        instSigGen.setAmpDBM(MV)  # set amplitude value from Cal File
        instSigGen.switchRFOn()  # set RF ON!!!!!!!!
        startTime = time.time()
        instPowerMeter.switchChannelA()
        instPowerMeter.getMeasVal()
        currFwdVal = instPowerMeter.currVal

        instPowerMeter.switchChannelB()
        instPowerMeter.getMeasVal()
        currRevVal = instPowerMeter.currVal
        currNetPower = currFwdVal-currRevVal
        k = 1
        print('Goal Fwd Value: %f' % setNetPower)
        iRow = 1
        tmpNetVal = [False] * 4
        while 1:
            if (setNetPower <= currNetPower <= setNetPower + netPowTol):
                tmpNetVal[iRow] = True
            else:
                tmpNetVal[iRow] = False
            print(tmpNetVal)
            iRow = iRow + 1
            if iRow > 3:
                iRow = 0

            if all(tmpNetVal):
                break
            instSigGen.setAmpDBM(MV)
            instPowerMeter.switchChannelA()
            instPowerMeter.getMeasVal()
            currFwdVal = instPowerMeter.currVal
            print('Current FWD Value: %f' % currFwdVal)

            instPowerMeter.switchChannelB()
            instPowerMeter.getMeasVal()
            currRevVal = instPowerMeter.currVal
            print('Current Rev Value: %f' % currRevVal)

            currNetPower = currFwdVal - currRevVal

            print('Current Net Value: %f' % currNetPower)
            t = time.time() - startTime
            MV = controller.send([t, currNetPower, setNetPower + netPowTol])
            print('Control MV Value: %f' % MV)
            k = k + 1
            plt.scatter(k, currNetPower)
            plt.show()
            plt.pause(0.001)

        controller.close()
        powFwdVal.append(currNetPower)
        plt.close()

# Abbruch calibration
elif testType == '4':
    print('4 selected')
    abortTest()

