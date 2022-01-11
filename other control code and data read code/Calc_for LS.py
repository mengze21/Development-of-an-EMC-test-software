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
aFile11 = open('LMK08.txt', 'r')
allLines11 = aFile11.readlines()

# print(allLines)
rowCnt = len(allLines11)-1
print(rowCnt)
kabel08F = [0] * rowCnt
kabel08Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines11[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel08F[i] = float(strList[0].replace(",", "."))  # 频率
    kabel08Mag[i] = float(strList[1].replace(",", "."))  # 幅度
#print(vectF)
#print(vectMag)
aFile12 = open('LMK09.txt', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12)-1
print(rowCnt)
kabel09F = [0] * rowCnt
kabel09Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel09F[i] = float(strList[0].replace(",", "."))  # 频率
    kabel09Mag[i] = float(strList[1].replace(",", "."))  # 幅度

aFile12 = open('LMK10.txt', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12) - 1
print(rowCnt)
kabel10F = [0] * rowCnt
kabel10Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    kabel10F[i] = float(strList[0].replace(",", "."))  # 频率
    kabel10Mag[i] = float(strList[1].replace(",", "."))  # 幅度

aFile = open('CDN_M316.POW', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-29
print(rowCnt)
REMIKF = [0] * rowCnt
REMIKMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIKF[i] = float(strList[0].replace(",", "."))*1000000  # 频率
    REMIKMag[i] = float(strList[1].replace(",", "."))  # 幅度
print(REMIKF)
#Antena=np.interp(F, vectF, vectMag)
kabel08=np.interp(REMIKF,kabel08F,kabel08Mag)
kabel09=np.interp(REMIKF,kabel09F,kabel09Mag)
kabel10=np.interp(REMIKF,kabel10F,kabel10Mag)
print(kabel08)
real= REMIKMag-kabel08-kabel09-kabel10+53

plt.figure()
plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(REMIKF,real)
plt.plot(REMIKF,REMIKMag)
#plt.plot(F1,M1)
#plt.plot(REMIF1,REMIMag1)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
plt.legend(['Umrechnung_Kalib-Wert_Rohdaten_LS','Kalib-Wert_Rohdaten_LS'], loc='upper left')  #'Python_Real_LE','Python_rohdaten_LE',
plt.show()