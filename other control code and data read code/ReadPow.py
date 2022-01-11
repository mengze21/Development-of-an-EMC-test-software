import numpy

#a= numpy.loadtxt(r"C:\Users\zzhang\PycharmProjects\pythonProject2\AF3m.txt")
#a= numpy.loadtxt('AF3m.txt', delimiter=',', usecols=range(2))
#print(a)
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
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    strList = lineText.split()  # 分割为字符串列表
    REMIKF[i] = float(strList[0].replace(",", "."))  # 频率
    REMIKMag[i] = float(strList[1].replace(",", "."))  # 幅度


for i in range(len(REMIKF)):
    print(i)
    print(REMIKF[i])
    print(REMIKMag[i])