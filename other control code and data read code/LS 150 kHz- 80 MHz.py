import pyvisa
from time import sleep  # for delays
import numpy as np
import matplotlib.pyplot as plt

aFile = open('CDN_M316.POW', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-29
print(rowCnt)
REMIKF = [0] * rowCnt
REMIKMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()                  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()                         # 分割为字符串列表
    REMIKF[i] = float(strList[0].replace(",", "."))    # 频率
    REMIKMag[i] = float(strList[1].replace(",", "."))  # 幅度
print(REMIKF)
print(len(REMIKF))
print(REMIKMag)


rm = pyvisa.ResourceManager()
print(rm.list_resources())

gpib_addr2='GPIB0::21::INSTR'
gpib_addr3='GPIB0::9::INSTR'
SignalGenerator=rm.open_resource(gpib_addr2)
HpSwitch=rm.open_resource(gpib_addr3)

SignalGenerator.write('AM S1 S4')     # für KNW
SignalGenerator.write('AM S2 S4')
SignalGenerator.write('AM S3 S4')
SignalGenerator.write('FR 1 MZ')

HpSwitch.write('OLAP 0')
HpSwitch.write('CLOSE 101')
HpSwitch.write('CMON 1')

SignalGenerator.write('R3')
SignalGenerator.write('FR 0.15 MZ')

frequenz = []
magnitude = []

for i in range(len(REMIKF)):
    #print(i)
    #print(REMIKF[i])
    print(REMIKMag[i])
    FR= REMIKF[i]
    AP= REMIKMag[i]
    SignalGenerator.write('FR %s MZ'% str(FR))
    SignalGenerator.write('AP %s DM'% str(AP))
    frequenz.append(FR)
    sleep(1)

SignalGenerator.write('AP -50 DM')
SignalGenerator.write('R2')

HpSwitch.write('OLAP 0')
HpSwitch.write('OPEN 101')
HpSwitch.write('CMON 1')




# The following is a drawing, not related to control
plt.figure()
plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(frequenz,magnitude)
plt.plot(REMIKF,REMIKMag)
#plt.plot(F1,M1)
#plt.plot(REMIF1,REMIMag1)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
plt.legend(['Power Meter_Rohdaten_LS','Kalib-Wert_Rohdaten_LS'], loc='upper left')  #'Python_Real_LE','Python_rohdaten_LE',
plt.show()

b=list(zip(frequenz,magnitude))

file=open('Power Meter_Rohdaten_LS.txt','w')
for i in b:
    file.write(str(i)+'\n')
file.close()