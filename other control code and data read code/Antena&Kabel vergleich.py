

# -*- coding: utf-8 -*-
import pyvisa
from time import sleep  # for delays
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#REMI Antenna
aFile = open('REMI_Antennenfaktor.COA', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
AntenaFREMI = [0] * rowCnt
AntenaMREMI = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    AntenaFREMI[i] = float(strList[0].replace(",", "."))  # 频率
    AntenaMREMI[i] = float(strList[1].replace(",", "."))  # 幅度

#print(AntenaFREMI)
#print(AntenaMREMI)

#REMI Kabel
aFile = open('REMI_Kabeldämpfung.CO2', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
KabelFREMI = [0] * rowCnt
KabelMREMI = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    KabelFREMI[i] = float(strList[0].replace(",", "."))  # 频率
    KabelMREMI[i] = float(strList[1].replace(",", "."))  # 幅度

#print(AntenaFREMI)
#print(AntenaMREMI)


### von Laura
## Kabel11
aFile11 = open('LMK11.txt', 'r')
allLines11 = aFile11.readlines()

# print(allLines)
rowCnt = len(allLines11)-1
#print(rowCnt)
kabel11F = [0] * rowCnt
kabel11Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines11[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel11F[i] = float(strList[0].replace(",", ".")) /1000000 # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度
#print(vectF)
#print(vectMag)

#Kabel12
aFile12 = open('LMK12.txt', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12)-1
#print(rowCnt)
kabel12F = [0] * rowCnt
kabel12Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel12F[i] = float(strList[0].replace(",", "."))  /1000000 # 频率
    kabel12Mag[i] = float(strList[1].replace(",", "."))  # 幅度


KabelMvonLaura=np.array(kabel11Mag)+np.array(kabel12Mag)

#print(kabel12Mag+kabel11Mag)
#print(len(kabel11Mag))
#print(len(kabel12Mag))
#KabelMvonLaura= kabel11Mag+kabel12Mag
#print(len(KabelMvonLaura))

##Antenna
aFile = open('AF3m.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
AntenaF = [0] * rowCnt
AntenaMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    AntenaF[i] = float(strList[0].replace(",", "."))  # 频率
    AntenaMag[i] = float(strList[1].replace(",", "."))  # 幅度

ax= plt.axes(xscale='log')

plt.subplot(2,1,1)

plt.plot(AntenaF,AntenaMag)
plt.plot(AntenaFREMI,AntenaMREMI)
plt.legend(['Antenenfaktor von Laura','Antenennfaktor von REMI'], loc='upper left')

plt.subplot(2,1,2)

plt.plot(kabel12F,KabelMvonLaura)
plt.plot(KabelFREMI,KabelMREMI)
plt.legend(['Kabeldämpfung von Laura','Kabeldämpfung von REMI'], loc='upper left')

plt.show()

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


rowCnt1 = len(allLines1[::2])-27  # 文本行数
vectF1_AVG = [0] * rowCnt1
vectMag1_AVG = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+26].strip()                 # 一行的文字，必须去掉末尾的\n
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


rowCnt1 = len(allLines1[::2])-27  # 文本行数
vectF1_QPE = [0] * rowCnt1
vectMag1_QPE = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+26].strip()                 # 一行的文字，必须去掉末尾的\n
    strList1 = lineText1.split(";",1)                   # 通过;分割为2份
    vectF1_QPE[i] = float(strList1[0])/1000000                     # 频率
    vectMag1_QPE[i] = float(strList1[1].replace(";", " "))  # 幅度