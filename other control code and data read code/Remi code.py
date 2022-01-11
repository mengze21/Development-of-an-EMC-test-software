# -*- coding: utf-8 -*-
import pyvisa
import numpy as np
import time
from time import sleep
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# data von python-selbst
aFile = open('code selbst_50 ms_10 db_ein_Label_first_plus Dampfung.txt', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-1
print(rowCnt)
selbstcodeF = [0] * rowCnt
selbstcodeMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    selbstcodeF[i] = float(strList[0].replace(",", ""))  # 频率
    selbstcodeMag[i] = float(strList[1])  # 幅度


#REMI1
aFile = open('WM_01_00min.TO1', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIF1 = [0] * rowCnt
REMIMag1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF1[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag1[i] = float(strList[1].replace(",", "."))  # 幅度

#print(REMIF)
#print(REMIMag)

#REMI2
aFile = open('WM_02_30min.TO1', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIF2 = [0] * rowCnt
REMIMag2 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF2[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag2[i] = float(strList[1].replace(",", "."))  # 幅度

#REMI3
aFile = open('WM_03_60min.TO2', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIF3 = [0] * rowCnt
REMIMag3 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF3[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag3[i] = float(strList[1].replace(",", "."))  # 幅度



#REMI4
aFile = open('WM_04_90min.TO3', 'r')
allLines = aFile.readlines()

print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIF4 = [0] * rowCnt
REMIMag4 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF4[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag4[i] = float(strList[1].replace(",", "."))  # 幅度


##Antenna
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
    kabel11F[i] = float(strList[0].replace(",", "."))/1000000  # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度
#print(vectF)
#print(vectMag)

# kabel12
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
    kabel12F[i] = float(strList[0].replace(",", "."))/1000000  # 频率
    kabel12Mag[i] = float(strList[1].replace(",", "."))  # 幅度

rm = pyvisa.ResourceManager()
print(rm.list_resources())
gpib_addr='GPIB0::20::INSTR'
gpib_inst=rm.open_resource(gpib_addr)
gpib_inst.timeout = 3000                # needs to be longer as sweep duration
print(gpib_inst.query('*IDN?'))          # print the device information
gpib_inst.write('*CLS')

gpib_inst.write('*RST;*WAI')
gpib_inst.write('INST REC')
gpib_inst.write('FREQ:MODE CW;*WAI')                     # in receiver mode, CW: single frequency measurement, SCAN: scan
gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
gpib_inst.write('SYST:DISP:UPD ON')   # in remi off
gpib_inst.write('DISP:ANN:FREQ ON')

#gpib_inst.write('DET:REC POS; *WAI')
#gpib_inst.write('DISP:TRAC:Y 50dB;*WAI')
#gpib_inst.write('BAND:RES 120 KHZ')
#gpib_inst.write('SWEEP:TIME 50 ms')
#gpib_inst.write('INP:ATT:AUTO OFF;*WAI')
#gpib_inst.write('INP:ATT:PROT OFF;*WAI')
#gpib_inst.write('INP:ATT 5DB;*WAI')
#gpib_inst.write('INP:ATT:AUTO ON;*WAI')
#gpib_inst.write('INP:ATT:AUTO:MODE LON;*WAI')
#gpib_inst.write('INP:GAIN:STAT ON;*WAI')

gpib_inst.write('DET:REC POS; *WAI')
gpib_inst.write('DISP:TRAC:Y 50dB;*WAI')
gpib_inst.write('BAND:RES 120 KHZ')
gpib_inst.write('SWEEP:TIME 20 ms')
#gpib_inst.write('INP:ATT:AUTO OFF;*WAI')               #
gpib_inst.write('INP:ATT:PROT OFF;*WAI')
gpib_inst.write('INP:ATT 0 DB;*WAI')
gpib_inst.write('INP:ATT:AUTO ON;*WAI')
gpib_inst.write('INP:ATT:AUTO:MODE LON;*WAI')
gpib_inst.write('INP:GAIN:STAT ON;*WAI')                  # The preamplifier can be switched on/off separately for each subrange

# gpib_inst.write('OUPT OFF')      # von REMI

#gpib_inst.write('FREP:CW 30 MHZ;*WAI')
#gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
#gpib_inst.write('INIT:CONT OFF')
#gpib_inst.write('INIT:IMM;*WAI')
#gpib_inst.write('FORM ASC;*WAI')
#messdaten=gpib_inst.query('TRAC? SINGLE;*WAI')
#print(messdaten)



rowCnt = len(np.arange(30.0,1000,0.12))-1
print(rowCnt)
vectF1 = [0] * rowCnt
vectMag1 = [0] * rowCnt

for i in range(rowCnt):
    #gpib_inst.write('*CLS')

    #print(i)
    start='30+0.12*i'
    #gpib_inst.write('FREQ:STAR %s MHz', start)
    gpib_inst.write('FREQ:CENT %s MHZ;*WAI',start)
    gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
    gpib_inst.write('INIT:CONT OFF')
    gpib_inst.write('INIT:IMM;*WAI')
    gpib_inst.write('FORM ASC;*WAI')
    messdaten = gpib_inst.query_ascii_values('TRAC? SINGLE;*WAI')
    print("{}  {}".format(30+0.12*i, messdaten))

    vectF1[i] = float(30+0.12*i)
    print(vectF[i])
    vectMag1[i] = float(str(messdaten[0]))
    print(vectMag[i])
#print(vectF)
#print(vectMag1)
#print(len(vectF))
#print(len(vectMag))
Antena=np.interp(vectF1, vectF, vectMag)
kabel11=np.interp(vectF1,kabel11F,kabel11Mag)
kabel12=np.interp(vectF1,kabel12F,kabel12Mag)
real= vectMag1+Antena-kabel11-kabel12-0
#print(real)


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




plt.plot(vectF1, real)
#plt.plot(selbstcodeF, selbstcodeMag)
plt.plot(REMIF1,REMIMag1)
plt.plot(REMIF2,REMIMag2)
plt.plot(REMIF3,REMIMag3)
plt.plot(REMIF4,REMIMag4)
#plt.legend(['python','python code wie remi'], loc='upper left')
#plt.legend(['python','REMI_00min','REMI_30min','REMI_60min','REMI_90min'], loc='upper left')
plt.legend(['python code wie remi','REMI_00min','REMI_30min','REMI_60min','REMI_90min'], loc='upper left')
# plt.tight_layout()
plt.show()

z=list(zip(vectF1,vectMag1))
#print(z)
#for line in lines:
#...
#fp.close()
#a=np.transpose(vectF1)
#b=np.transpose(vectMag1)
#print(vectF1.shape)
file=open('remi code rohdaten_second.txt','w')
for i in z:
    file.write(str(i)+'\n')
file.close()



