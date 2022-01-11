aFile = open('./data/CDN_M316.POW', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-29
#print(rowCnt)
F1 = [0] * rowCnt
M1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+29].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split()  # 分割为字符串列表
    F1[i] = float(strList[0].replace(",", ""))*1000 # 频率
    M1[i] = float(strList[1]) +10 # 幅度

print(len(F1))
print(M1)