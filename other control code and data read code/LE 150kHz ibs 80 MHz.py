# -*- coding: utf-8 -*-
import pyvisa
from time import sleep  # for delays
import pandas as pd
import numpy as np
from collections import Iterable
import matplotlib.pyplot as plt

'''##Antenna
aFile = open('AF3m.txt', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-1
print(rowCnt)
vectF = [0] * rowCnt
vectMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    vectF[i] = float(strList[0].replace(",", "."))  # 频率
    vectMag[i] = float(strList[1].replace(",", "."))  # 幅度'''

## K
aFile11 = open('LMK11.txt', 'r')
allLines11 = aFile11.readlines()

# print(allLines)
rowCnt = len(allLines11)-1
print(rowCnt)
kabel11F = [0] * rowCnt
kabel11Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines11[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel11F[i] = float(strList[0].replace(",", "."))  # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度
#print(vectF)
#print(vectMag)
aFile12 = open('LMK12.txt', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12)-1
print(rowCnt)
kabel12F = [0] * rowCnt
kabel12Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel12F[i] = float(strList[0].replace(",", "."))  # 频率
    kabel12Mag[i] = float(strList[1].replace(",", "."))  # 幅度

rm = pyvisa.ResourceManager()
print(rm.list_resources())
gpib_addr='GPIB0::20::INSTR'
gpib_inst=rm.open_resource(gpib_addr)
gpib_inst.timeout = 30000                # needs to be longer as sweep duration
print(gpib_inst.query('*IDN?'))          # print the device information
gpib_inst.write('*CLS')                  # clear all status

# set the initial parameter

gpib_inst.write('INST:SEL REC')            # reveiver mode; SAN spectrum mode
gpib_inst.write('DSIP:PSAVe OFF')          # switches on or off the power-save mode of the display
gpib_inst.write('SYST:DISP:UPD ON')        # Display during remote control ON
gpib_inst.write('INIT:DISP OFF')           # This command configures the behavior of the display during a single sweep.
                                           # The numeric suffix of INITiate is irrelevant with this command
                                           # OFF: the display is switched off during the measurement,
                                           # ON: the display is switched on during the measurement
gpib_inst.write('CALC:UNIT:POW DBUV ')     # unit

gpib_inst.write('DISP:WIND1:SEL')             # Selects screen A as active measurement window; WIND2: screen B

# gpib_inst.write('DISP:WIND:TRAC1:MODE POS')   # Trace1 PK+ (von Matlab code , i think it's wrong)
gpib_inst.write('DISP:WIND:TRAC1:MODE WRIT')    # trace1 mode:WRIT: Clear and write; WRITe | VIEW | AVERage | MAXHold | MINHold
#gpib_inst.write('DISP:WIND:TRAC2:MODE WRIT')    # trace2 mode:WRIT: Clear and write; WRITe | VIEW | AVERage | MAXHold | MINHold
gpib_inst.write(':DISP:WIND:TRAC:Y:RLEV 50')    # y relevant 50 db
# gpib_inst.write(':DET1 POS')
#gpib_inst.write('DET1:REC POS')                 # detector1 Max peak
gpib_inst.write(':DET1 POS')                # detector2 average; QPE: Quasipeak
gpib_inst.write('DET1:REC POS')                # detector2 average; QPE: Quasipeak
gpib_inst.write(':INIT2:CONT ON')               # selects the continuous scan/sweep mode; OFF: single scan/sweep
gpib_inst.write('SWE:SPAC LIN')

gpib_inst.write('FREQ:STAR 30 MHz')  # start frequency of display range
gpib_inst.write('FREQ:STOP 1000 MHz')  # stop frequency of display range (not useful)

# schritte 1 von 30 bis 60


F=[]
M=[]
count=1
for t in range(0,2,1):

    if count == 0 :

        for i in range(150,1000,50):

            #gpib_inst.write('*CLS')
            gpib_inst.write('SCAN:RANG:COUN 1')
            start= i
            print(i)
            stop= i+50
            #print(start)
            #print(stop)
            gpib_inst.write('SWE:SPAC LIN')

            gpib_inst.write('FREQ:STAR %s kHz'% str(start))  # start frequency of display range
            gpib_inst.write('FREQ:STOP %s kHz'% str(stop))  # stop frequency of display range
            gpib_inst.write('SCAN1:STAR %s kHz;*WAI'% str(start))  # entry of start frequency
            gpib_inst.write('SCAN1:STOP %s kHz;*WAI'% str(stop))  # entry of stop frequency
            #gpib_inst.write('SCAN1:STEP AUTO')
            gpib_inst.write('SCAN1:STEP 2.4 kHz')  # entry of step size
            gpib_inst.write(':BAND:TYPE PULS')  # 6 dB??
            gpib_inst.write('SCAN1:BAND:RES 9 kHz')  # entry of IF Bandwidth
            gpib_inst.write('SCAN1:TIME 50 ms')  # measurement time
            gpib_inst.write('INP:ATT:AUTO OFF')
            gpib_inst.write('INP:ATT:PROT OFF')
            gpib_inst.write('INP:ATT 0 DB')
            gpib_inst.write('SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
            gpib_inst.write('SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
            gpib_inst.write('SCAN1:INP:ATT 0 dB')  # entry of a fixed RF attenuation (0 db,10 db 50 db)
            gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  # von remi
            gpib_inst.write('SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
            gpib_inst.write('SCAN1:INP:GAIN:STAT ON')  # The preamplifier can be switched on/off separately for each subrange
            # gpib_inst.write('SCAN1:INP:GAIN:AUTO OFF')     # Auto ranging without preamplification
            # gpib_inst.write('OUPT OFF') # von remi
            # gpib_inst.write('FREQ:CENT:STEP:LINK OFF')    # This command couples the step width of the center frequency to span (span >0) or to the resolution bandwidth (span = 0) or cancels the couplings.
            # OFF = manual input, no coupling (from matlab code, make sense or not?)

            gpib_inst.write('TRAC:FEED:CONT ALW')  # SCAN results available
            gpib_inst.write('FORM ASC')  # specifies the data format
            gpib_inst.write('FORM:DEXP:DSEP POIN')  # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
             # gpib_inst.write('SCAN:RANG:COUN 1')           # determines the number of ranges.

            gpib_inst.write('INIT2;*WAI')  # start the scan

            sleep(2)
            gpib_inst.write(':ABOR')

            gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')  # save trace1 data to PK.ASC
            #gpib_inst.write('MMEM:STOR1:TRAC 2,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
            #gpib_inst.write('MMEM:STOR1:TRAC 3,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC

            gpib_inst.write('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"')
            data_PK = gpib_inst.read('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"').split(";")[48:]
            print(data_PK)
            frequenz = []
            magnitude = []
            for x in data_PK:
                 if len(x) >= 10:
                    frequenz.append(float(x.replace('\r\n',''))/1000000.0)
                 else:
                    if x != '\r\n\n':
                        magnitude.append(float(x))
            F.extend(frequenz)
            M.extend(magnitude)

            print(frequenz)
            print(magnitude)

    elif count == 1:
        startfre=2000
        for i in range(startfre/1000, 30, 1):
            gpib_inst.write('SCAN:RANG:COUN 1')
            t = []
            # gpib_inst.write('*CLS')
            start = i
            print(i)
            stop = i + 1
            # print(start)
            # print(stop)
            gpib_inst.write('FREQ:STAR %s MHz' % str(start))  # start frequency of display range
            gpib_inst.write('FREQ:STOP %s MHz' % str(stop))  # stop frequency of display range (not useful)
            gpib_inst.write('SCAN1:STAR %s MHz;*WAI' % str(start))  # entry of start frequency
            gpib_inst.write('SCAN1:STOP %s MHz;*WAI' % str(stop))  # entry of stop frequency
            # gpib_inst.write('SCAN1:STEP AUTO')
            gpib_inst.write('SCAN1:STEP 10 kHz')  # entry of step size
            gpib_inst.write(':BAND:TYPE PULS')  # 6 dB??
            gpib_inst.write('SCAN1:BAND:RES 10 kHz')  # entry of IF Bandwidth
            gpib_inst.write('SCAN1:TIME 50 ms')  # measurement time
            gpib_inst.write('INP:ATT:AUTO OFF')
            gpib_inst.write('INP:ATT:PROT OFF')
            gpib_inst.write('INP:ATT 0 DB')
            gpib_inst.write('SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
            gpib_inst.write('SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
            gpib_inst.write('SCAN1:INP:ATT 0 dB')  # entry of a fixed RF attenuation (0 db,10 db 50 db)
            gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  # von remi
            gpib_inst.write('SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
            gpib_inst.write('SCAN1:INP:GAIN:STAT ON')  # The preamplifier can be switched on/off separately for each subrange
            # gpib_inst.write('SCAN1:INP:GAIN:AUTO OFF')     # Auto ranging without preamplification
            # gpib_inst.write('OUPT OFF') # von remi
            # gpib_inst.write('FREQ:CENT:STEP:LINK OFF')    # This command couples the step width of the center frequency to span (span >0) or to the resolution bandwidth (span = 0) or cancels the couplings.
            # OFF = manual input, no coupling (from matlab code, make sense or not?)

            gpib_inst.write('TRAC:FEED:CONT ALW')  # SCAN results available
            gpib_inst.write('FORM ASC')  # specifies the data format
            gpib_inst.write(
                'FORM:DEXP:DSEP POIN')  # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
            # gpib_inst.write('SCAN:RANG:COUN 1')           # determines the number of ranges.

            gpib_inst.write('INIT2;*WAI')  # start the scan

            sleep(5.2)
            gpib_inst.write(':ABOR')

            gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')  # save trace1 data to PK.ASC
            # gpib_inst.write('MMEM:STOR1:TRAC 2,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
            # gpib_inst.write('MMEM:STOR1:TRAC 3,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC

            gpib_inst.write('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"')
            data_PK = gpib_inst.read('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"').split(";")[48:]
            print(type(data_PK))

            frequenz1 = []
            magnitude1 = []
            for x in data_PK:

                if len(x) >= 13:
                    frequenz1.append(float(x.replace('\r\n', '')) / 1000000.0)
                else:
                    if x != '\r\n\n':
                        magnitude1.append(float(x))
            F.extend(frequenz1)
            M.extend(magnitude1)
            print(frequenz1)
            print(magnitude1)
            #print(F)
            #print(M)
    count=count+1
    print(count)

print(F)
print(M)




#Antena=np.interp(F, vectF, vectMag)
kabel11=np.interp(F,kabel11F,kabel11Mag)
kabel12=np.interp(F,kabel12F,kabel12Mag)
real= M-kabel11-kabel12

plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
# a1 = plt.subplot(311)
# a1.set_title("间隔")
# a1.set_ylabel("time(s)")
# plt.axis([30, 1000, -5, 65])
# my_x_ticks = np.arange(-5, 5, 0.5)

plt.plot(F, real)
# plt.tight_layout()
plt.show()

z=list(zip(F,real))

file=open('Python_Real_LE.txt','w')
for i in z:
    file.write(str(i)+'\n')
file.close()

b=list(zip(F,M))

file=open('Python_rohdaten_LE.txt','w')
for i in b:
    file.write(str(i)+'\n')
file.close()