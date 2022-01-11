import numpy

#a= numpy.loadtxt(r"C:\Users\zzhang\PycharmProjects\pythonProject2\AF3m.txt")
#a= numpy.loadtxt('AF3m.txt', delimiter=',', usecols=range(2))
#print(a)
import numpy as np
import matplotlib.pyplot as plt

aFile = open('Netznachbildung S11_L.CSV', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-3
print(rowCnt)
vectF = [0] * rowCnt
vectMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    vectF[i] = float(strList[0]) /1000 # 频率
    vectMag[i] = float(strList[1])  # 幅度

print(vectF)
print(vectMag)


font2={'family':'Times New Roman',
       'weight':'normal',

       'size': 30,
       }

plt.figure()
plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.tick_params(labelsize=30)
#plt.plot(F1,M1)
#plt.plot(F2,M2)
plt.plot(vectF,vectMag)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
#legend= plt.legend(prop=font2)
plt.legend(['Netznachbildung S11_L'], loc='upper left',title_fontsize='30',fontsize = 20)  #'Python_Real_LE','Python_rohdaten_LE',
plt.xlabel('Frequenz / kHz',font2)
plt.ylabel('S11 / dB',font2)
plt.show()
#print(vectF)
#print(vectMag)
#with open('AF3m.txt', 'r') as f:
 #   data = f.readlines()  # txt中所有字符串读入data

#print(data)
#self.chart.removeAllSeries()
#rowCnt = len(data)-1
