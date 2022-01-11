import numpy as np

import matplotlib.pyplot as plt
#REMI
aFile = open('KABEL.CO2', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-30
print(rowCnt)
REMIKF = [0] * rowCnt
REMIKMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIKF[i] = float(strList[0].replace(",", "."))  # 频率
    REMIKMag[i] = float(strList[1].replace(",", "."))  # 幅度




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

#KabelvonBeidenM=kabel12Mag+kabel11Mag

def list_add(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i])
    return c
KabelvonBeidenM= list_add(kabel12Mag,kabel11Mag)
plt.figure()
plt.axis([0,3000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(kabel12F,KabelvonBeidenM)

plt.plot(REMIKF,REMIKMag)
plt.grid()
plt.legend(['Kabeldämpfung von K11 und K12','Kabeldämpfung von Remi_LE'], loc='upper left')  #'receiver mode code',
plt.show()