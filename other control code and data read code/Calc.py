# -*- coding: utf-8 -*-
import pyvisa
from time import sleep  # for delays
# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''aFile1 = open('Receiver mode code Rohdaten_first.txt', 'r')
allLines1 = aFile1.readlines()
aFile1.close()
#print(len(allLines1))
#print(allLines1[::2])
ALLdata=allLines1[::2]
#print(len(allLines1[::2]))


rowCnt1 = len(allLines1[::2])-27  # 文本行数
vectF1 = [0] * rowCnt1
vectMag1 = [0] * rowCnt1
for i in range(rowCnt1):                             # 文本中26行的冗余

    lineText1 = ALLdata[i+26].strip()                 # 一行的文字，必须去掉末尾的\n
    strList1 = lineText1.split(";",1)                   # 通过;分割为2份
    vectF1[i] = float(strList1[0])/1000000                     # 频率
    vectMag1[i] = float(strList1[1].replace(";", " "))  # 幅度'''

# Python_Real_LE
aFile = open('Python_Real_LE.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F1 = [0] * rowCnt
M1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F1[i] = float(strList[0].replace(",", ""))  # 频率
    M1[i] = float(strList[1])  # 幅度

# Python-Average-V
aFile = open('Python_rohdaten_LE.txt', 'r')
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
    M2[i] = float(strList[1])  # 幅度

'''# Python-Max-H
aFile = open('Python-Max-H_rohdaten_0 dB_2 mal.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F3 = [0] * rowCnt
M3 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F3[i] = float(strList[0].replace(",", ""))  # 频率
    M3[i] = float(strList[1])  # 幅度'''


#REMI1-Max-V
aFile = open('LE_NUL_.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIF1 = [0] * rowCnt
REMIMag1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF1[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag1[i] = float(strList[1].replace(",", "."))  # 幅度

#REMI1-Max-V
aFile = open('LE_NUL_Gross.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIF2 = [0] * rowCnt
REMIMag2 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF2[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag2[i] = float(strList[1].replace(",", "."))  # 幅度
#print(REMIF)
#print(REMIMag)

'''#REMI2-Quasi-V
aFile = open('REMI-Quasi-V.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIF2 = [0] * rowCnt
REMIMag2 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF2[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag2[i] = float(strList[1].replace(",", "."))  # 幅度

#REMI Average-V
aFile = open('REMI-AVER-V.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIF3 = [0] * rowCnt
REMIMag3 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF3[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag3[i] = float(strList[1].replace(",", "."))  # 幅度

#print(REMIF)
#print(REMIMag)

#REMI-Max-H
aFile = open('REMI-MAX-H.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIF4 = [0] * rowCnt
REMIMag4 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIF4[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMag4[i] = float(strList[1].replace(",", "."))  # 幅度'''

'''#REMI ROH
aFile = open('ROHDATEN.TO1', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
#print(rowCnt)
REMIFROH = [0] * rowCnt
REMIMagROH = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIFROH[i] = float(strList[0].replace(",", "."))  # 频率
    REMIMagROH[i] = float(strList[1].replace(",", "."))  # 幅度'''
#print(REMIFROH)
#print(REMIMagROH)
#print(REMIF)
#print(REMIMag)

'''##Antenna
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
    AntenaMag[i] = float(strList[1].replace(",", "."))  # 幅度'''

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


# Antena=np.interp(REMIF1, AntenaF, AntenaMag)
kabel11=np.interp(REMIF1,kabel11F,kabel11Mag)
#print(kabel11)
kabel12=np.interp(REMIF1,kabel12F,kabel12Mag)
#real1= vectMag1+Antena


remi_max= REMIMag1-kabel11-kabel12
#real3= vectMag1+Antena+kabel11+kabel12

# Antena_Kabel=Antena-kabel11-kabel12

#Antenaremi=np.interp(REMIF2, AntenaF, AntenaMag)
#kabel11remi=np.interp(REMIF2,kabel11F,kabel11Mag)
#print(kabel11)
#kabel12remi=np.interp(REMIF2,kabel12F,kabel12Mag)
#real1= vectMag1+Antena
#remi_quasi= REMIMag2+Antena-kabel11-kabel12
#remi_average= REMIMag3+Antena-kabel11-kabel12
#remi_max_H=REMIMag4+Antena-kabel11-kabel12


#Antenapython=np.interp(F1, AntenaF, AntenaMag)
#kabel11python=np.interp(F1,kabel11F,kabel11Mag)
#print(kabel11)
#kabel12python=np.interp(F1,kabel12F,kabel12Mag)

#python_max_V= M1+Antenapython-kabel11python-kabel12python
#python_max_H=M3+Antenapython-kabel11python-kabel12python


#Antenapython_av=np.interp(F2, AntenaF, AntenaMag)
#kabel11python_av=np.interp(F2,kabel11F,kabel11Mag)
#print(kabel11)
#kabel12python_av=np.interp(F2,kabel12F,kabel12Mag)

#python_average_V=M2+Antenapython_av-kabel11python_av-kabel12python_av






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
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 30,
         }

plt.figure()
#plt.axis([0.15,30,-5,65])
#my_y_ticks = np.arange(-20, 65, 10)
  # plt.xticks(my_x_ticks)
#plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.tick_params(labelsize=20)
plt.plot(REMIF1,REMIMag1)
plt.plot(F2,M2)
#设置坐标轴范围
plt.xlim((0, 50))
plt.ylim((-20,60))
#设置坐标轴名称
plt.xlabel('Frequenz / MHz',font2)
plt.ylabel('Störspannung / dBµV',font2)
#设置坐标轴刻度
#my_x_ticks = np.arange(-20, 80, 10)
#对比范围和名称的区别
#my_x_ticks = np.arange(-5, 2, 0.5)
my_y_ticks = np.arange(-20, 80, 10)
#plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

#plt.plot(F1,M1)
#plt.plot(REMIF1,REMIMag1)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
legend = plt.legend(prop=font2)
plt.legend(['REMI_Nullmessung_Rohdaten','Python_Nullmessung_Rohdaten'], loc='upper left',title_fontsize ='30',fontsize = 30)  #'Python_Real_LE','Python_rohdaten_LE',

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
#c=list(zip(frequenz,ESPImessdaten))

file=open('ESPI Messdaten(Kalib.Wert==Kalib.Wert).txt','w')
for i in c:
    file.write(str(i)+'\n')
file.close()