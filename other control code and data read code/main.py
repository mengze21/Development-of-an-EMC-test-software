# -*- coding: utf-8 -*-
import pyvisa
import numpy as np
import time
from time import sleep
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker


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
print(gpib_inst.query('*IDN?'))
#gpib_inst.write('*IDN?')
#while True:
#print(gpib_inst.read_bytes(1))
#gpib_inst.baud_rate= 9600

gpib_inst.write_termination ='\n'
gpib_inst.read_termination = '\n'

# set the initial parameter
# set the initial parameter
#gpib_inst.write('FREQ:STAR 30 MHz')            # start frequency of display range (not useful)
#gpib_inst.write('FREQ:STOP 1 GHz')             # stop frequency of display range (not useful)



# set the initial parameter
gpib_inst.write(':SYS:PRES')
gpib_inst.write('*OPT?')
gpib_inst.write(':INST SAN;:CALC:UNIT:POW dBuV;:SYST:DISP:UPD ON;:INP:PRES:STAT ON;:BAND:TYPE PULS')   # san mode ;preselection on
gpib_inst.write('*OPT?')
# gpib_inst.write('INST:SEL SAN')                # selection of receiver mode
gpib_inst.write('*IDN?')   # selection of receiver mode
gpib_inst.write('*OPT?')
gpib_inst.write(':INP:GAIN:STAT OFF')           # start frequency of display range (not useful)
gpib_inst.write(':INIT:CONT OFF')             # stop frequency of display range (not useful)
gpib_inst.write(':SWE:POIN 8001')
# gpib_inst.write(':SWE:POIN 501')

gpib_inst.write(':FREQ:STAR 30 MHz;:FREQ:STOP 1 GHz;')                # selection of receiver mode
gpib_inst.write(':SWE:TIME 50 s')                 # selection of receiver mode
gpib_inst.write(':DISP:WIND:TRAC:Y:RLEV 50;:INP:ATT:AUTO ON;')

gpib_inst.write(':BAND:RES 120 kHz;:BAND:VID:AUTO ON')             # stop frequency of display range (not useful)
gpib_inst.write(':DET POS')
gpib_inst.write(':AVER:COUN 1;:DISP:TRAC1:MODE WRIT')

gpib_inst.write('INP:ATT:PROT OFF')
gpib_inst.write('INP:ATT 0 DB')

gpib_inst.write('*CLS;:INIT:IMM;*OPC')                 # selection of receiver mode

v = 0
while v <= 50.0:

    sleep(0.1)
    vMeasured = gpib_inst.query_ascii_values('TRAC1:IMM:RES?', converter='f')   # measure the dBµV (y result); TRAC1:IMM:RES? can returns the x and y result, but right now i don't know how to seperate it
    gpib_inst.query('*ESR?')
    # Write results to console
    print("{}  {}".format(v, vMeasured))

    v += 0.1

 # gpib_inst.write(':ABOR')


a= gpib_inst.query_ascii_values(':TRAC:DATA? TRACE1')
print(a)
print(len(a))

# x = np.arange(30,999.88,1.93612774)   ##501
# x = np.arange(30,1000.1,0.1212)
x = np.arange(30,999.79,0.1212121212) ## 8001
Antena=np.interp(x, vectF, vectMag)
kabel11=np.interp(x,kabel11F,kabel11Mag)
kabel12=np.interp(x,kabel12F,kabel12Mag)
real= a+Antena-kabel11-kabel12
print(x)
print(len(x))


plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 5)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
# a1 = plt.subplot(311)
# a1.set_title("间隔")
# a1.set_ylabel("time(s)")
# plt.axis([30, 1000, -5, 65])
# my_x_ticks = np.arange(-5, 5, 0.5)

plt.plot(x, real)
# plt.tight_layout()
plt.show()

#bins = np.linspace(30, 1000, 50) #横坐标起始和结束值，分割成21份
#plt.figure(figsize=(13,5)) #图像大小
#plt.xticks(bins) #设置x轴
#plt.xlim(30, 1000) #x轴开始和结束位置

# T = np.arctan2(a,x)
# plt.scatter(x,a,s = 5,c = 'r',alpha = .5)
#plt.plot(x,a)
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
#plt.tight_layout()
#plt.show()



# gpib_inst.write(':ABOR')
