from csv import reader
import csv
import math

listCsvFile = []
listNormalizedCsvFile = []
listForwardCal = []
listCalResult = []
def createCalibrationFile(listCsvFile):
    E_T = 3  # Prüffeldstärke
    E_L = E_T * 1.8  # Pegeleinstellungsfeldstärke
    polarisation = 'vertical'
    currPoint = 1
    for csvEl in listCsvFile:
        with open(csvEl, 'r') as read_obj:
            csv_reader = reader(read_obj)
            listCalFile = list(csv_reader)

            if currPoint == 1:
                minLength = len(listCalFile)
            if minLength >= len(listCalFile):
                minLength = len(listCalFile)
            #print(listCalFile)
            rowSize = len(listCalFile)
            #print(rowSize)
            #print(listCalFile[rowSize - 1][1])
            # 0 = Frequencyf
            # 1 = Forward Power
            # 2 = Reverse Power
            # 3 = Power Signal Generator
            # 4 = Electric Field Strength

            # normalize the values
            for row in listCalFile:
                diffDbm = 20*math.log(float(row[4])/E_L)
                row[1] = float(row[1])-diffDbm
                row[2] = float(row[2])-diffDbm
                row[3] = float(row[3])-diffDbm
                row[4] = E_L

            path = 'normalized_ output_%s_%i.csv' % (polarisation, currPoint)
            listNormalizedCsvFile.append(path)
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for l in listCalFile:
                    writer.writerow(l)
            currPoint = currPoint + 1
    for i in range(0,minLength):
        listForwardCal.clear()
        for csvEl in listNormalizedCsvFile:
            with open(csvEl, 'r') as read_obj:
                csv_reader = reader(read_obj)
                listCalFile = list(csv_reader)
                listForwardCal.append(float(listCalFile[i][1]))
        sortedList = sorted(listForwardCal)
        min = sortedList[0]
        max = sortedList[-1]  # index -1 will give the last element#
        diff  = max - min
        if (diff) < 6:
            listCalResult.append([float(listCalFile[i][0]), max - 5.1, float(listCalFile[i][2]) - 5.1, float(listCalFile[i][3]) - 5.1, float(listCalFile[i][4]) / 1.8, 1])
        else:
            print("Failed: difference:", diff)
            print( "min", min, listForwardCal.index(min))
            print( "max", max, listForwardCal.index(max))
            listCalResult.append([float(listCalFile[i][0]), max - 5.1, float(listCalFile[i][2]) - 5.1, float(listCalFile[i][3])-5.1, float(listCalFile[i][4])/1.8, 0])

    path = 'calResult.csv'
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for l in listCalResult:
            writer.writerow(l)

listCsvFile.append('output_vertical_1.csv')
listCsvFile.append('output_vertical_2.csv')
listCsvFile.append('output_vertical_3.csv')
listCsvFile.append('output_vertical_4.csv')
listCsvFile.append('output_vertical_5.csv')
createCalibrationFile(listCsvFile)