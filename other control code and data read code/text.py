#REMI1
aFile = open('REMI-MAX-V.TO1', 'r')
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

print(REMIF1)
print(REMIMag1)