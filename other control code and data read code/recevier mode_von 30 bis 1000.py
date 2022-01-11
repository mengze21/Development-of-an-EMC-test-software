# -*- coding: utf-8 -*-
import pyvisa
from time import sleep  # for delays
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#REMI4
aFile = open('WM_04_90min.TO3', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIF4 = [0] * rowCnt
REMIMag4 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF4[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag4[i] = float(strList[1].replace(",", "."))  # 幅度

#print(REMIF)
#print(REMIMag)
#print(REMIF)
#print(REMIMag)

## Antenna
aFile = open('AF3m.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
print(rowCnt)
vectF = [0] * rowCnt
vectMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    vectF[i] = float(strList[0].replace(",", "."))  # 频率
    vectMag[i] = float(strList[1].replace(",", "."))  # 幅度

## Kabel11
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
    kabel11F[i] = float(strList[0].replace(",", ".")) /1000000 # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度
#print(vectF)
#print(vectMag)

## Kabel12
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
    kabel12F[i] = float(strList[0].replace(",", ".")) /1000000 # 频率
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

gpib_inst.write('DISP:ANN:FREQ ON')        ## von remi

gpib_inst.write('DISP:WIND1:SEL')             # Selects screen A as active measurement window; WIND2: screen B

# gpib_inst.write('DISP:WIND:TRAC1:MODE POS')   # Trace1 PK+ (von Matlab code , i think it's wrong)
gpib_inst.write('DISP:WIND:TRAC1:MODE WRIT')    # trace1 mode:WRIT: Clear and write; WRITe | VIEW | AVERage | MAXHold | MINHold
gpib_inst.write('DISP:WIND:TRAC2:MODE WRIT')    # trace2 mode:WRIT: Clear and write; WRITe | VIEW | AVERage | MAXHold | MINHold
gpib_inst.write('DISP:WIND:TRAC3:MODE WRIT')    # trace2 mode:WRIT: Clear and write; WRITe | VIEW | AVERage | MAXHold | MINHold
gpib_inst.write(':DISP:WIND:TRAC:Y:RLEV 50')    # y relevant 50 db
# gpib_inst.write(':DET1 POS')
gpib_inst.write('DET1:REC POS')                 # detector1 Max peak
gpib_inst.write('DET2:REC AVER')                # detector2 average; QPE: Quasipeak
gpib_inst.write('DET3:REC QPE')
gpib_inst.write(':INIT2:CONT ON')               # selects the continuous scan/sweep mode; OFF: single scan/sweep

gpib_inst.write('DISP:TRAC:Y 50dB;*WAI') # von remi 和上面的相似

gpib_inst.write('SWE:SPAC LIN') 
gpib_inst.write('FREQ:STAR 30 MHz')             # start frequency of display range
gpib_inst.write('FREQ:STOP 1000 MHz')              # stop frequency of display range (not useful)
gpib_inst.write('SCAN1:STAR 30 MHz')            # entry of start frequency
gpib_inst.write('SCAN1:STOP 500 MHz')          # entry of stop frequency
gpib_inst.write('SCAN1:STEP AUTO')
gpib_inst.write('SCAN1:STEP 120 kHz')           # entry of step size
gpib_inst.write(':BAND:TYPE PULS')              # 6 dB??
gpib_inst.write('SCAN1:BAND:RES 120 kHz')       # entry of IF Bandwidth
gpib_inst.write('SCAN1:TIME 20 ms')              # measurement time
gpib_inst.write('SCAN1:INP:ATT:AUTO OFF')       # Auto Ranging off: the input attenuation setting of the scan table is used
gpib_inst.write('SCAN1:INP:ATT 20 dB')           # entry of a fixed RF attenuation (0 db,10 db 50 db)
gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  #von remi
gpib_inst.write('SCAN1:INP:ATT:PROT OFF')       # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
gpib_inst.write('SCAN1:INP:GAIN:STAT ON')       # The preamplifier can be switched on/off separately for each subrange
#gpib_inst.write('SCAN1:INP:GAIN:AUTO OFF')     # Auto ranging without preamplification
#gpib_inst.write('OUPT OFF') # von remi
# gpib_inst.write('FREQ:CENT:STEP:LINK OFF')    # This command couples the step width of the center frequency to span (span >0) or to the resolution bandwidth (span = 0) or cancels the couplings.
                                                # OFF = manual input, no coupling (from matlab code, make sense or not?)

gpib_inst.write('TRAC:FEED:CONT ALW')           # SCAN results available
gpib_inst.write('FORM ASC')                     # specifies the data format
gpib_inst.write('FORM:DEXP:DSEP POIN')          # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
# gpib_inst.write('SCAN:RANG:COUN 1')           # determines the number of ranges.

gpib_inst.write('INIT2;*WAI')                   # start the scan


sleep(100)
gpib_inst.write(':ABOR')

gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')     # save trace1 data to PK.ASC
gpib_inst.write('MMEM:STOR1:TRAC 2,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
gpib_inst.write('MMEM:STOR1:TRAC 3,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC

#gpib_inst.write('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"')
#gpib_inst.write('MMEM:DATA? "D:\Matlab_Directory\AVG.ASC"')
#gpib_inst.write('MMEM:DATA? "D:\Matlab_Directory\QPE.ASC"')
data_PK=gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"')        # read trace1 data
data_AVG=gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\AVG.ASC"')        # read trace2 data
data_QPE=gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\QPE.ASC"')        # read trace3 data
print(data_PK)
print(data_AVG)
print(data_QPE)

# PK DATA
fp=open('Receiver mode code Rohdaten_PK.txt','w')
fp.write(data_PK)
fp.close


aFile1 = open('Receiver mode code Rohdaten_PK.txt', 'r')
allLines1 = aFile1.readlines()
aFile1.close()
print(len(allLines1))
#print(allLines1[::2])
ALLdata=allLines1[::2]
print(len(allLines1[::2]))


rowCnt1 = len(allLines1[::2])-38  # 文本行数
vectF1_PK = [0] * rowCnt1
vectMag1_PK = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+37].strip()                 # 一行的文字，必须去掉末尾的\n
    strList1 = lineText1.split(";",1)   # 通过;分割为2份
    if strList1[0]!='':
        print(strList1)

        vectF1_PK[i] = float(strList1[0])/1000000                     # 频率
        vectMag1_PK[i] = float(strList1[1].replace(";", " "))  # 幅度

print(vectF1_PK)
print(vectMag1_PK)
#AVG DATA
#print(vectMag1)

fp=open('Receiver mode code Rohdaten_AVG.txt','w')
fp.write(data_AVG)
fp.close


aFile1 = open('Receiver mode code Rohdaten_AVG.txt', 'r')
allLines1 = aFile1.readlines()
aFile1.close()
print(len(allLines1))
#print(allLines1[::2])
ALLdata=allLines1[::2]
print(len(allLines1[::2]))


rowCnt1 = len(allLines1[::2])-38  # 文本行数
vectF1_AVG = [0] * rowCnt1
vectMag1_AVG = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+37].strip()                 # 一行的文字，必须去掉末尾的\n
    strList1 = lineText1.split(";",1)                   # 通过;分割为2份
    vectF1_AVG[i] = float(strList1[0])/1000000                     # 频率
    vectMag1_AVG[i] = float(strList1[1].replace(";", " "))  # 幅度



#QPE DATA
#print(vectMag1)

fp=open('Receiver mode code Rohdaten_QPE.txt','w')
fp.write(data_QPE)
fp.close


aFile1 = open('Receiver mode code Rohdaten_QPE.txt', 'r')
allLines1 = aFile1.readlines()
aFile1.close()
print(len(allLines1))
#print(allLines1[::2])
ALLdata=allLines1[::2]
print(len(allLines1[::2]))


rowCnt1 = len(allLines1[::2])-38  # 文本行数
vectF1_QPE = [0] * rowCnt1
vectMag1_QPE = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+37].strip()                 # 一行的文字，必须去掉末尾的\n
    strList1 = lineText1.split(";",1)                   # 通过;分割为2份
    vectF1_QPE[i] = float(strList1[0])/1000000                     # 频率
    vectMag1_QPE[i] = float(strList1[1].replace(";", " "))  # 幅度'''


Antena=np.interp(vectF1_QPE, vectF, vectMag)
kabel11=np.interp(vectF1_QPE,kabel11F,kabel11Mag)
kabel12=np.interp(vectF1_QPE,kabel12F,kabel12Mag)

real_PK= vectMag1_PK+Antena-kabel11-kabel12-20
real_AVG= vectMag1_AVG+Antena-kabel11-kabel12-20
real_QPE= vectMag1_QPE+Antena-kabel11-kabel12-20
#print(x)
#print(len(x))


plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
# a1 = plt.subplot(311)
# a1.set_title("间隔")
# a1.set_ylabel("time(s)")
# plt.axis([30, 1000, -5, 65])
# my_x_ticks = np.arange(-5, 5, 0.5)

#plt.subplot(3,1,1)
plt.plot(vectF1_PK, real_PK)
plt.plot(vectF1_AVG, real_AVG)
plt.plot(vectF1_QPE, real_QPE)
#plt.plot(remicodeF, remicodeMag)
#plt.plot(REMIF1,REMIMag1)
#plt.plot(REMIF2,REMIMag2)
#plt.plot(REMIF3,REMIMag3)
#plt.plot(REMIF4,REMIMag4)
#plt.legend(['python','python code wie remi'], loc='upper left')
plt.legend(['PK','AVG','QPE','REMI_90min_PK'], loc='upper left')
#plt.legend(['python','python code wie remi','REMI_00min','REMI_30min','REMI_60min','REMI_90min'], loc='upper left')
# plt.tight_layout()
plt.show()


#z=list(zip(vectF1,real))
#print(z)
#for line in lines:
#...
#fp.close()
#a=np.transpose(vectF1)
#b=np.transpose(vectMag1)
#print(vectF1.shape)
#file=open('testdata.txt','w')
#for i in z:
#    file.write(str(i)+'\n')
#file.close()