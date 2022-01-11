# -*- coding: utf-8 -*-
import pyvisa
from time import sleep  # for delays
# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
#20 dB 注意单位 每个都确认一遍
aFile = open('20 DB DÄMPFUNGSGLIED.CSV', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-3
#print(rowCnt)
vectF1 = [0] * rowCnt
vectMag1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    vectF1[i] = float(strList[0])/1000000  # 频率
    vectMag1[i] = float(strList[1])  # 幅度
print('20dB')
print(vectF1)
print(vectMag1)

#10 DB
aFile = open('TRACE01 10 DB.CSV', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-3
#print(rowCnt)
vectF = [0] * rowCnt
vectMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    vectF[i] = float(strList[0])/1000000  # 频率
    vectMag[i] = float(strList[1])  # 幅度
print('10dB')
print(vectF)
print(vectMag)
#

aFile = open('CDN_M316.POW', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-29
#print(rowCnt)
REMIKF = [0] * rowCnt
REMIKMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIKF[i] = float(strList[0].replace(",", "."))  # 频率
    REMIKMag[i] = float(strList[1].replace(",", "."))  # 幅度


# Kalib.Wert=-30
aFile = open('ESPI Messdaten(Kalib.Wert==Kalib.Wert_KZANGE)_1.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)
#print(rowCnt)
F1 = [0] * rowCnt
M1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F1[i] = float(strList[0].replace(",", "")) # 频率
    M1[i] = float(strList[1])  # 幅度
print('F1')
print(F1)
print(M1)

# Kalib.Wert==Kalib.Wert
'''aFile = open('ESPI Messdaten(Kalib.Wert==Kalib.Wert).txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F2 = [0] * rowCnt
M2 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F2[i] = float(strList[0].replace(",", ""))  # 频率
    M2[i] = float(strList[1])  # 幅度'''


## Kabel11
aFile11 = open('LMK 11 9KHZ-100MHZ.CSV', 'r')
allLines11 = aFile11.readlines()
# print(allLines)
rowCnt = len(allLines11)-3
#print(rowCnt)
kabel11F = [0] * rowCnt
kabel11Mag = [0] * rowCnt
for i in range(rowCnt):

    lineText = allLines11[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1 = lineText.replace("(", "")
    lineText2 = lineText1.replace(")", "")
    # print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    kabel11F[i] = float(strList[0].replace(",", ".")) /1000000 # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度
print('LMK11')
print(kabel11F)
print(kabel11Mag)

#Kabel12
aFile12 = open('LMK 12 9KHZ-100MHZ.CSV', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12)-3
#print(rowCnt)
kabel12F = [0] * rowCnt
kabel12Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1 = lineText.replace("(", "")
    lineText2 = lineText1.replace(")", "")
    # print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    kabel12F[i] = float(strList[0].replace(",", "."))  /1000000 # 频率
    kabel12Mag[i] = float(strList[1].replace(",", "."))  # 幅度
print('LMK12')
print(kabel12F)
print(kabel12Mag)

# Antena=np.interp(REMIF1, AntenaF, AntenaMag)
kabel11=np.interp(F1,kabel11F,kabel11Mag)
print(kabel11)

kabel12=np.interp(F1,kabel12F,kabel12Mag)
print(kabel12)
Dämpfung10=np.interp(F1,vectF,vectMag)
Dämpfung20=np.interp(F1,vectF1,vectMag1)
print(Dämpfung10)
print(Dämpfung20)


#print(M1)
print(20*math.log(3,10))
Spannung_EUT= M1-kabel11-kabel12-Dämpfung10-Dämpfung20+20*math.log(3,10)
#print(Spannung_EUT)
Abweichung=140-Spannung_EUT


Kalibrieung_Wert_CDN=-30+Abweichung
length=len(Kalibrieung_Wert_CDN)
print(length)
Kalibrieung=[0]*length

for i in range(length):

    Kalibrieung[i] = Kalibrieung_Wert_CDN[i]
print(len(F1))
print(len(Kalibrieung))
'''#print(len(REMI))
#minus=real2remi-REMI

plt.figure()
plt.axis([30,3000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')

plt.plot(REMIF1,remi_max)
plt.plot(REMIF2, remi_quasi)
plt.plot(REMIF3, remi_average)
plt.plot(REMIF4, remi_max_H)
plt.plot(REMIF1,REMIMag1)
plt.plot(REMIF2, REMIMag2)
plt.plot(REMIF3, REMIMag3)
plt.plot(REMIF4, REMIMag4)

plt.grid()
plt.legend(['Max-V-REMI_Rohdaten','Qua-V-REMI_Rohdaten','Aver-V-REMI_Rohdaten','Max-H-REMI_Rohdaten',], loc='upper left')  #'receiver mode code',

plt.show()


plt.figure()
plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')

#plt.subplot(3,1,1)
#plt.axis([30,1000,-5,65])

plt.plot(F1,python_max_V)
plt.plot(F2, python_average_V)
plt.plot(F3, python_max_H)
plt.plot(F1,M1)
plt.plot(F2, M2)
plt.plot(F3, M3)
#plt.plot(REMIF4, real_max_H)

plt.grid()
plt.legend(['Max-V-Python_Rohdaten','Aver-V-Python_Rohdaten','Max-H-Python_Rohdaten'], loc='upper left')  #'receiver mode code',
#plt.legend(['roh daten','+Antena','+Antena-Dampfung ','+Antena+Dampfung','Remi_90min'], loc='upper left')
#plt.legend(['remi code','REMI_90min'], loc='upper left') # 'REMI_0min','REMI_30min','REMI_60min',
# plt.tight_layout()

plt.show()'''


plt.figure()
plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(F1,M1)
#plt.plot(F2,M2)
#plt.plot(F1,M1)
plt.plot(REMIKF,REMIKMag)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
plt.legend(['Kalib.Wert=-30','(Kalib.Wert==Kalib.Wert_RSUS)','Kalib.Wert_RSUS'], loc='upper left')  #'Python_Real_LE','Python_rohdaten_LE',
plt.show()

'''plt.figure()
plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(F3,python_max_H)
plt.plot(REMIF4,remi_max_H)
plt.grid()
plt.legend(['Max-H-Python','Max-H-REMI'], loc='upper left')  #'receiver mode code',
plt.show()

plt.figure()
plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(F2,python_average_V)
plt.plot(REMIF3,remi_average)
plt.grid()
plt.legend(['Average-V-Python','Average-V-REMI'], loc='upper left')  #'receiver mode code',
plt.show()
'''

c=list(zip(F1,Kalibrieung))

file=open('Kalib.Wert_KZANGE.txt','w')
for i in c:
    file.write(str(i)+'\n')
file.close()