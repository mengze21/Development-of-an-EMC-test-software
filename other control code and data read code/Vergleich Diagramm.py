import matplotlib.pyplot as plt
import numpy as np

## 10 db
aFile = open('receiver_mode_10db.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_10db = [0] * rowCnt
M_10db = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_10db[i] = float(strList[0].replace(",", ""))  # 频率
    M_10db[i] = float(strList[1])  # 幅度

aFile = open('receiver_mode_10db_rohdaten.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_10db_roh = [0] * rowCnt
M_10db_roh = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_10db_roh[i] = float(strList[0].replace(",", ""))  # 频率
    M_10db_roh[i] = float(strList[1])  # 幅度


## 0 db
aFile = open('receiver_mode_0db.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_0db = [0] * rowCnt
M_0db = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_0db[i] = float(strList[0].replace(",", ""))  # 频率
    M_0db[i] = float(strList[1])  # 幅度

aFile = open('receiver_mode_0db_rohdaten.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_0db_roh = [0] * rowCnt
M_0db_roh = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_0db_roh[i] = float(strList[0].replace(",", ""))  # 频率
    M_0db_roh[i] = float(strList[1])  # 幅度

## 20 db
aFile = open('receiver_mode_20db.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_20db = [0] * rowCnt
M_20db = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_20db[i] = float(strList[0].replace(",", ""))  # 频率
    M_20db[i] = float(strList[1])  # 幅度

aFile = open('receiver_mode_20db_rohdaten.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
#print(rowCnt)
F_20db_roh = [0] * rowCnt
M_20db_roh = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F_20db_roh[i] = float(strList[0].replace(",", ""))  # 频率
    M_20db_roh[i] = float(strList[1])  # 幅度


plt.axis([30,1000,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')


#plt.subplot(2,1,1)
plt.plot(F_0db, M_0db)
plt.plot(F_10db, np.array(M_10db)+10)
plt.plot(F_20db, np.array(M_20db)+20)

#plt.plot(F_0db_roh, M_0db_roh)
#plt.plot(F_10db_roh, M_10db_roh)
#plt.plot(F_20db_roh, M_20db_roh)
#plt.plot(F2, M2)
#plt.plot(REMIF4,REMIMag4)
#plt.legend(['code selbst_50 ms_10 db_ein_Label_minus Dampfung','code selbst_50 ms_10 db_ein_Label_first_plus Dampfung','Remi_WM_04_90min'], loc='upper left')


#plt.legend(['code wie REMI_50 ms_10 db_ein_Label_minus Dampfung','code wie REMI_50 ms_10 db_ein_Label_Plus Dampfung','Remi_WM_04_90min'], loc='upper left')
#plt.plot(REMIF3,REMIMag3)
#plt.plot(REMIF4,REMIMag4)

#plt.legend(['code selbst_50 ms_10 db_ein_Label_minus Dampfung','code selbst_50 ms_10 db_ein_Label_first_plus Dampfung'], loc='upper left')
plt.legend(['receiver 0 Db','receiver 10 Db','receiver 20 Db'], loc='upper left')
#plt.legend(['receiver 0 Db_roh','receiver 10 Db_roh','receiver 20 Db_roh',], loc='upper left')
# plt.tight_layout()
plt.show()