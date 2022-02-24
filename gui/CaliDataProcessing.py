# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def caliDataProcessing():
    data = ["", "", "", "", "", ""]
    # read all data
    for i in range(1, 6):
        data[i] = pd.read_csv('data/Calibration_FS/output_vertical_%s.csv' % i, header=None).values
    data1 = np.array((data[1]))
    data2 = np.array((data[2]))
    data3 = np.array((data[3]))
    data4 = np.array((data[4]))
    data5 = np.array((data[5]))
    # split data into 5 column
    # column 2 is powFwdVal, column 3 is powRwdVal
    splitData1 = np.hsplit(data1, 5)
    splitData2 = np.hsplit(data2, 5)
    splitData3 = np.hsplit(data3, 5)
    splitData4 = np.hsplit(data4, 5)
    splitData5 = np.hsplit(data5, 5)
    # stack the value of all 5 positions in one array
    powFwdVal = np.hstack((splitData1[1], splitData2[1], splitData3[1], splitData4[1], splitData5[1]))
    powRevVal = np.hstack((splitData1[2], splitData2[2], splitData3[2], splitData4[2], splitData5[2]))
    sondeListVal = np.hstack((splitData1[4], splitData2[4], splitData3[4], splitData4[4], splitData5[4]))
    # find the maximum
    maxPowFwdVal = np.amax(powFwdVal, axis=1, out=None, keepdims=True)
    #print(powFwdVal)
    #print(maxPowFwdVal)
    #print("len data %s" % len(data5))
    #print("len maxPowFwdVal %s" % len(maxPowFwdVal))

    result = np.hstack((data1, data2, data3, data4, data5))
    result = np.concatenate((result, maxPowFwdVal), axis=1)
    print("result %s" % result)
    #writeF = pd.DataFrame(result)
    return result
    #np.savetxt('data/Calibration_FS/Calibration_result.csv', result)

