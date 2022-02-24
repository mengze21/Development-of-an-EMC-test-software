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
from WrapperEMRFeldsonde import WrapperEMRFeldsonde

#plot stuiff

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2

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
instWrapperEMR = WrapperEMRFeldsonde("ASRL3::INSTR", rm) # Adresse als Variable von GUI übernehmen

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
        # print('P: %f' % P)
        # print('I: %f' % I)
        MV = MV_bar + P + I

        # print('New MV: %f' % MV)
        # update stored data for next iteration
        t_prev = t




# Read the csv file as rows in the list.
# Format is the following frequency, Forward Power , Reverse Power, Power for the SignalGenerator, Electric Field Strength.
with open('calResult.csv', 'r') as read_obj:
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
    # 5 = Cal Success Status

    plt.ion()  ## Note this correction
    fig = plt.figure()
    plt.title("Field Strength Control")
    plt.xlabel("Step")
    plt.ylabel("Field Strength")
    plt.axis([0, 200, -3, 10])
    plt.axhline(y=(3), color='r', linestyle='-')
    k = 1
    for x in listCalFile:
        setFrequ = float(x[0])
        setAPM = float(x[3])
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
        instSigGen.switchRFOn()  # set RF ON!!!!!!!
        instWrapperEMR.readval()
        plt.scatter(k, instWrapperEMR.effEVal)
        plt.show()
        plt.pause(0.001)
        instSigGen.switchAPModulationON()
        time.sleep(maxStayTime)
        plt.scatter(k, instWrapperEMR.effEVal, marker=',')
        k = k + 1
        plt.show()
        plt.pause(0.001)
        instSigGen.switchAPModulationOFF()




# Forward Power Calibration
elif testType == '2':
    fwdTol = 0.1
    print('2 selected')
    plt2.ion()
    fig2 = plt2.figure()
    plt2.title("Field Strength Control")
    plt2.xlabel("Step")
    plt2.ylabel("Field Strength")
    plt2.axis([0, 200, -3, 10])
    plt2.axhline(y=(3), color='r', linestyle='-')

    j = 1
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
        plt.axis([0, 200, -35, -10])
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
        # print('Goal Fwd Value: %f' % setFwdPow)
        iRow = 1
        tmpFwdVal = [False] * 4
        while 1:
            if (setFwdPow < currFwdVal < setFwdPow + fwdTol ):
                tmpFwdVal[iRow] = True
            else:
                tmpFwdVal[iRow] = False

            # print(tmpFwdVal)
            iRow = iRow + 1
            if iRow > 3:
                iRow = 0

            if all(tmpFwdVal):
                break

            instSigGen.setAmpDBM(MV)
            instPowerMeter.getMeasVal()
            currFwdVal = instPowerMeter.currVal
            # print('Current Fwd Value: %f' % currFwdVal)
            t = time.time() - startTime
            MV = controller.send([t, currFwdVal, setFwdPow + 0.05])
            # print('Control MV Value: %f' % MV)
            k = k + 1
            plt.scatter(k, currFwdVal)
            plt.show()
            plt.pause(0.001)
        plt.close()
        instWrapperEMR.readval()
        print(instWrapperEMR.effEVal)
        plt2.scatter(j, instWrapperEMR.effEVal)
        plt2.show()
        plt2.pause(0.001)
        instSigGen.switchAPModulationON()
        time.sleep(maxStayTime)
        print('T',instWrapperEMR.effEVal)
        plt2.scatter(j, instWrapperEMR.effEVal, marker=',')
        j = j + 1
        plt2.show()
        plt2.pause(0.001)
        instSigGen.switchAPModulationOFF()
        controller.close()
        powFwdVal.append(currFwdVal)



elif testType == '3':
    print('3 selected')
    netPowTol = 0.3
    plt2.ion()
    fig2 = plt2.figure()
    plt2.title("Field Strength Control")
    plt2.xlabel("Step")
    plt2.ylabel("Field Strength")
    plt2.axis([0, 200, -3, 10])
    plt2.axhline(y=(3), color='r', linestyle='-')

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
        plt.axis([0, 200, -15, 15])
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
        # print('Goal Fwd Value: %f' % setNetPower)
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

            # print('Current Net Value: %f' % currNetPower)
            t = time.time() - startTime
            MV = controller.send([t, currNetPower, setNetPower + netPowTol])
            # print('Control MV Value: %f' % MV)
            k = k + 1
            plt.scatter(k, currNetPower)
            plt.show()
            plt.pause(0.001)
            instWrapperEMR.readval()
            print(instWrapperEMR.effEVal)

        plt.close()
        instWrapperEMR.readval()
        print(instWrapperEMR.effEVal)
        plt2.scatter(j, instWrapperEMR.effEVal)
        plt2.show()
        plt2.pause(0.001)
        instSigGen.switchAPModulationON()
        time.sleep(maxStayTime)
        print('T', instWrapperEMR.effEVal)
        plt2.scatter(j, instWrapperEMR.effEVal, marker=',')
        j = j + 1
        plt2.show()
        plt2.pause(0.001)
        instSigGen.switchAPModulationOFF()
        controller.close()
        powFwdVal.append(currNetPower)

# Abbruch calibration
elif testType == '4':
    print('4 selected')
    abortTest()

