import numpy as np
import matplotlib.pyplot as plt
import math


# Kalib.Wert=-30
aFile = open('ESPI Rechung_Daten(Kalib.Wert==Kalib.Wert_CDN)_1..txt', 'r')
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


'''length=len(F1)
#print(length)
V=[0]*length
for i in range(length):

    V[i] =math.pow(10, M1[i])

print(V)'''

V=[ 10**((i-120)/20) for i in M1]   ##math.pow*(float(10),float((i-120)/20))

print(V)
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 30,
         }

plt.figure()
#plt.axis([0.15,80,9,12])
#my_y_ticks = np.arange(9, 12, 0.1)
  # plt.xticks(my_x_ticks)
#plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.tick_params(labelsize=20)
#plt.plot(F1,M1)
#plt.plot(F2,M2)
#plt.plot(F1,M1)
plt.plot(F1,V)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
legend = plt.legend(prop=font2)
plt.legend(['Spannung bei EUT_Koppelnetzwerk'], loc='upper left',title_fontsize ='30',fontsize = 30)  #'Python_Real_LE','Python_rohdaten_LE',
plt.xlabel('Frequenz / MHz',font2)
plt.ylabel('Spannung / V',font2)
plt.show()




