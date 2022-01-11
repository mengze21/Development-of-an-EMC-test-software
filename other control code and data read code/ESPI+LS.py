import pyvisa
from time import sleep  # for delays
import numpy as np
import matplotlib.pyplot as plt
import math

#20 dB
aFile = open('20 DB DÄMPFUNGSGLIED.CSV', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-3

vectF1 = [0] * rowCnt
vectMag1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    vectF1[i] = float(strList[0]) /1000000 # 频率
    vectMag1[i] = float(strList[1])  # 幅度

#
#10 DB
aFile = open('TRACE01 10 DB.CSV', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-3

vectF = [0] * rowCnt
vectMag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    #print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    vectF[i] = float(strList[0]) /1000000# 频率
    vectMag[i] = float(strList[1])  # 幅度

## Kabel11
aFile11 = open('LMK 11 9KHZ-100MHZ.CSV', 'r')
allLines11 = aFile11.readlines()
# print(allLines)
rowCnt = len(allLines11)-3
#print(rowCnt)
kabel11F = [0] * rowCnt
kabel11Mag = [0] * rowCnt
for i in range(rowCnt):

    lineText = allLines11[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1 = lineText.replace("(", "")
    lineText2 = lineText1.replace(")", "")
    # print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    kabel11F[i] = float(strList[0].replace(",", ".")) /1000000 # 频率
    kabel11Mag[i] = float(strList[1].replace(",", "."))  # 幅度

#Kabel12
aFile12 = open('LMK 12 9KHZ-100MHZ.CSV', 'r')
allLines12 = aFile12.readlines()

# print(allLines)
rowCnt = len(allLines12)-3
#print(rowCnt)
kabel12F = [0] * rowCnt
kabel12Mag = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines12[i+3].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1 = lineText.replace("(", "")
    lineText2 = lineText1.replace(")", "")
    # print(lineText2)
    strList = lineText2.split(',')  # 分割为字符串列表
    kabel12F[i] = float(strList[0].replace(",", "."))  /1000000 # 频率
    kabel12Mag[i] = float(strList[1].replace(",", "."))  # 幅度


aFile = open('Kalib.Wert_KZANGE.txt', 'r')
allLines = aFile.readlines()

#print(allLines)
rowCnt = len(allLines)-1
print(rowCnt)
F1 = [0] * rowCnt
M1 = [0] * rowCnt
for i in range(rowCnt):
    lineText = allLines[i].strip()  # 一行的文字，必须去掉末尾的\n
    lineText1=lineText.replace("(","")
    lineText2=lineText1.replace(")","")
    strList = lineText2.split()  # 分割为字符串列表
    F1[i] = float(strList[0].replace(",", ""))  # 频率
    M1[i] = float(strList[1])  # 幅度



#M_kalib=[13.4-a for a in M1]
#print(M_kalib)

rm = pyvisa.ResourceManager()
print(rm.list_resources())
#gpib_addr='GPIB0::20::INSTR'
#gpib_inst=rm.open_resource(gpib_addr)
#gpib_inst.timeout = 30000                # needs to be longer as sweep duration
#print(gpib_inst.query('*IDN?'))          # print the device information
#gpib_inst.write('*CLS')                  # clear all status
gpib_addr1='GPIB0::11::INSTR'
gpib_addr2='GPIB0::21::INSTR'
gpib_addr3='GPIB0::9::INSTR'
PowerMeter=rm.open_resource(gpib_addr1)
SignalGenerator=rm.open_resource(gpib_addr2)
HpSwitch=rm.open_resource(gpib_addr3)
print(PowerMeter.query('*IDN?'))
print(SignalGenerator.query('*IDN?'))
print(HpSwitch.query('ID?'))


gpib_addr='GPIB0::20::INSTR'
gpib_inst=rm.open_resource(gpib_addr)
gpib_inst.timeout = 3000             # needs to be longer as sweep duration
print(gpib_inst.query('*IDN?'))          # print the device information
gpib_inst.write('*CLS')                  # clear all status

gpib_inst.read_termination = '\n'
gpib_inst.write_termination = '\n'
# set the initial parameter
gpib_inst.write('*RST;*WAI')
gpib_inst.write('INST REC')
gpib_inst.write('FREQ:MODE CW;*WAI')                     # in receiver mode, CW: single frequency measurement, SCAN: scan
gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
gpib_inst.write('SYST:DISP:UPD ON')   # in remi off
gpib_inst.write('DISP:ANN:FREQ ON')

'''gpib_inst.write('DET:REC POS; *WAI')
gpib_inst.write('DISP:TRAC:Y 50dB;*WAI')
gpib_inst.write('BAND:RES 120 KHZ')
gpib_inst.write('SWEEP:TIME 20 ms')
gpib_inst.write('INP:ATT:PROT OFF;*WAI')
gpib_inst.write('INP:ATT 0 DB;*WAI')
gpib_inst.write('INP:ATT:AUTO ON;*WAI')
gpib_inst.write('INP:ATT:AUTO:MODE LON;*WAI')
gpib_inst.write('INP:GAIN:STAT ON;*WAI')  '''


gpib_inst.write('DET:REC POS; *WAI')
gpib_inst.write('DISP:TRAC:Y 50dB;*WAI')
gpib_inst.write('BAND:RES 9 KHZ')
gpib_inst.write('SWEEP:TIME 20 ms')
gpib_inst.write('INP:ATT:PROT OFF;*WAI')
gpib_inst.write('INP:ATT 10 DB;*WAI')
gpib_inst.write('INP:ATT:AUTO ON;*WAI')
gpib_inst.write('INP:ATT:AUTO:MODE LON;*WAI')
gpib_inst.write('INP:GAIN:STAT ON;*WAI')
gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
gpib_inst.write('INIT:CONT ON')
gpib_inst.write('INIT:IMM;*WAI')
gpib_inst.write('FORM ASC;*WAI')


SignalGenerator.write('AM S1 S4')     # für KNW
SignalGenerator.write('AM S2 S4')
SignalGenerator.write('AM S3 S4')
SignalGenerator.write('FR 0.15 MZ')


PowerMeter.write('*RST')
PowerMeter.write('INP:NSEL 2')             # 1: FWD 2:REV
PowerMeter.write('SENS1:POW:UNIT dBm')     # V Messung von Spannung, dBm : Power level
PowerMeter.write('POW:ATT 50')
PowerMeter.write('CORR:FREF 80 MHz; STATE ON')

HpSwitch.write('OLAP 0')
HpSwitch.write('CLOSE 101')
HpSwitch.write('CMON 1')

'''SignalGenerator.write('R3')
SignalGenerator.write('FR 0.15 MZ')'''

frequenz = []
magnitude = []
ESPImessdaten=[]
ESPI_Rechnung_daten=[]
for i in range(len(F1)):
    #print(i)
    #print(REMIKF[i])
    #print(REMIKMag[i])
    if F1[i] >=0:
        FR= F1[i]
        AP=M1[i]
        #AP= -30

        SignalGenerator.write('FR %s MZ'% str(FR))
        SignalGenerator.write('AP %s DM'% str(AP))
        #print(FR)
        print('Kali.Wert=%f'%AP)
        frequenz.append(FR)
        #PowerMeter.write('CORR:FREF %s MHz; STATE ON'% str(FR))
        #PowerM=PowerMeter.query('MEAS?')
        #print('PowerMeter.Wert=%.8f' % float(PowerM.strip()))

        #magnitude.append(float(PowerM.strip()))

        #start = '30+0.12*i'
        # gpib_inst.write('FREQ:STAR %s MHz', start)
        #gpib_inst.write('FREP:CW 20 MHZ;*WAI')
        gpib_inst.write('FREQ:CENT %s MHZ;*WAI' % str(FR))
        gpib_inst.write('CALC:UNIT:POW DBUV;*WAI')
        gpib_inst.write('INIT:CONT OFF')
        gpib_inst.write('INIT:IMM;*WAI')
        gpib_inst.write('FORM ASC;*WAI')
        gpib_inst.write('TRAC? SINGLE;*WAI')
        messdaten=float(gpib_inst.read('TRAC? SINGLE;*WAI'))
        print(type(messdaten))
        print(messdaten)
        #messdaten = gpib_inst.query_ascii_values('TRAC? SINGLE;*WAI')[0]
        #messdaten = gpib_inst.query_ascii_values('TRAC? SINGLE;*WAI')
        print(messdaten)
        kabel11 = np.interp(FR, kabel11F, kabel11Mag)
        kabel12 = np.interp(FR, kabel12F, kabel12Mag)
        Dämpfung10 = np.interp(FR, vectF, vectMag)
        Dämpfung20 = np.interp(FR, vectF1, vectMag1)
        print(kabel11,kabel12,Dämpfung10,Dämpfung20,20*math.log(3,10))
        real_messdaten=messdaten-kabel11-kabel12-Dämpfung10-Dämpfung20+20*math.log(3,10)
        print('ESPI.Wert=%f' % messdaten)
        print('ESPI.Real.Wert=%f'%real_messdaten)
        print('/n')
        ESPImessdaten.append(messdaten)
        ESPI_Rechnung_daten.append(real_messdaten)
        #print(messdaten)

        sleep(1)

SignalGenerator.write('AP -50 DM')
SignalGenerator.write('R2')

HpSwitch.write('OLAP 0')
HpSwitch.write('OPEN 101')
HpSwitch.write('CMON 1')

plt.figure()
plt.axis([0.15,30,-5,65])
my_y_ticks = np.arange(-5, 65, 10)
  # plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
ax= plt.axes(xscale='log')
plt.plot(frequenz,ESPImessdaten)
plt.plot(frequenz,ESPI_Rechnung_daten)
plt.plot(F1,M1)
#plt.plot(F1,M1)
#plt.plot(REMIF1,REMIMag1)
#plt.plot(REMIF2,REMIMag2)
plt.grid()
plt.legend(['ESPI Messwert','ESPI Rechnung Wert','Kalib-Wert_KZANGE'], loc='upper left')  #'Python_Real_LE','Python_rohdaten_LE',
plt.show()

'''b=list(zip(frequenz,magnitude))

file=open('Power Meter_Rohdaten_LS.txt','w')
for i in b:
    file.write(str(i)+'\n')
file.close()'''

c=list(zip(frequenz,ESPImessdaten))

file=open('ESPI Messdaten(Kalib.Wert==Kalib.Wert_KZANGE)_1.txt','w')
for i in c:
    file.write(str(i)+'\n')
file.close()

d=list(zip(frequenz,ESPI_Rechnung_daten))

file=open('ESPI Rechung_Daten(Kalib.Wert==Kalib.Wert_KZANGE)_1.txt','w')
for i in d:
    file.write(str(i)+'\n')
file.close()