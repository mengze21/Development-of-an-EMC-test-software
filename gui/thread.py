# -*- coding: utf-8 -*-

import sys
sys.path.append('gui')
import time
from PyQt5.QtCore import QThread, pyqtSignal
import pyvisa


class External(QThread):
    countChanged = pyqtSignal(list, int)

    def __init__(self, mode,attenuation,messtime,startfre):
        super(External, self).__init__()
        self.mode = mode
        self.attenuation = attenuation
        self.messtime = messtime
        self.startfrequency = startfre
        self.signal =1
        self.count = 0
        self.rm = pyvisa.ResourceManager()
        self.gpib_addr = 'GPIB0::20::INSTR'
        self.gpib_inst = self.rm.open_resource(self.gpib_addr)
        self.gpib_inst.timeout = 30000  # needs to be longer as sweep duration
        self.gpib_inst.write('*CLS')
        self.gpib_inst.write('INST:SEL REC')  # reveiver mode; SAN spectrum mode
        self.gpib_inst.write('DSIP:PSAVe OFF')  # switches on or off the power-save mode of the display
        self.gpib_inst.write('SYST:DISP:UPD ON')  # Display during remote control ON
        self.gpib_inst.write('INIT:DISP OFF')  # This command configures the behavior of the display during a single sweep.
        self.gpib_inst.write('CALC:UNIT:POW DBUV ')  # unit
        self.gpib_inst.write('DISP:WIND1:SEL')  # Selects screen A as active measurement window; WIND2: screen B
        self.gpib_inst.write('DISP:WIND:TRAC1:MODE WRIT')
        self.gpib_inst.write(':DISP:WIND:TRAC:Y:RLEV 50')  # y relevant 50 db
        if self.mode == 'max':
            self.gpib_inst.write(':DET1 POS')
        elif self.mode == 'average':
            self.gpib_inst.write(':DET1 AVER')
        elif self.mode == 'quasi':
            self.gpib_inst.write(':DET1 QPE')
        self.gpib_inst.write(':INIT2:CONT ON')  # selects the continuous scan/sweep mode; OFF: single scan/sweep
        self.gpib_inst.write('SWE:SPAC LIN')
        self.gpib_inst.write('FREQ:STAR 30 MHz')  # start frequency of display range
        self.gpib_inst.write('FREQ:STOP 1000 MHz')  # stop frequency of display range (not useful)
        self.gpib_inst.write('SWE:SPAC LIN')

    def run(self):
        while self.count == 0 :
            if self.startfrequency < 1000:
                for i in range(self.startfrequency, 1000, 50):
                    print(i)
                    if (self.signal & 1) == 1:  #是奇数
                        start = i
                        stop = i + 50
                        stopfre=stop
                        self.gpib_inst.write('SCAN:RANG:COUN 1')
                        self.gpib_inst.write('FREQ:STAR %s KHz' % str(start))  # start frequency of display range
                        self.gpib_inst.write('FREQ:STOP %s KHz' % str(stop))  # stop frequency of display range
                        self.gpib_inst.write('SCAN1:STAR %s KHz;*WAI' % str(start))  # entry of start frequency
                        self.gpib_inst.write('SCAN1:STOP %s KHz;*WAI' % str(stop))  # entry of stop frequency
                        self.gpib_inst.write('SCAN1:STEP 2.4 kHz')  # entry of step size
                        self.gpib_inst.write(':BAND:TYPE PULS')  # 6 dB??
                        self.gpib_inst.write('SCAN1:BAND:RES 9 kHz')  # entry of IF Bandwidth
                        self.gpib_inst.write('SCAN1:TIME %d ms' % self.messtime)  # measurement time
                        self.gpib_inst.write('SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
                        self.gpib_inst.write('INP:ATT:AUTO OFF')
                        self.gpib_inst.write('INP:ATT:PROT OFF')
                        self.gpib_inst.write('INP:ATT %d DB' % self.attenuation)
                        self.gpib_inst.write(
                            'SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
                        self.gpib_inst.write(
                            'SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                        self.gpib_inst.write('SCAN1:INP:ATT %d dB' % self.attenuation)  # entry of a fixed RF attenuation (0 db,10 db 50 db)
                        self.gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  # von remi
                        self.gpib_inst.write('SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                        self.gpib_inst.write('SCAN1:INP:GAIN:STAT ON')  # The preamplifier can be switched on/off separately for each subrange
                        self.gpib_inst.write('TRAC:FEED:CONT ALW')  # SCAN results available
                        self.gpib_inst.write('FORM ASC')  # specifies the data format
                        self.gpib_inst.write('FORM:DEXP:DSEP POIN')  # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
                        self.gpib_inst.write('INIT2;*WAI')  # start the scan
                        if self.mode == 'max':
                            time.sleep(2)
                        elif self.mode == 'average':
                            time.sleep(2)
                        else:
                            time.sleep(40)
                        self.gpib_inst.write(':ABOR')
                        if self.mode == 'max':
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')  # save trace1 data to PK.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"').split(";")[48:]
                        elif self.mode == 'average':
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\AVG.ASC"').split(";")[48:]
                        else:
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\QPE.ASC"').split(";")[48:]
                        self.countChanged.emit(data_PK, stop)
                    else:
                        #self.gpib_inst.write(':ABOR;*WAI')  # stop the scan
                        self.startfrequency= stopfre
                        print(self.startfrequency)
                        self.gpib_inst.write(':ABOR;*WAI')
                        break
                self.count += 1

            elif self.startfrequency >= 1000:

                for i in range(self.startfrequency, 30000, 1000):
                    if (self.signal & 1) == 1:  #是奇数
                        start = i
                        stop = i + 1000
                        stopfre = stop
                        self.gpib_inst.write('SCAN:RANG:COUN 1')
                        self.gpib_inst.write('FREQ:STAR %s KHz' % str(start))  # start frequency of display range
                        self.gpib_inst.write('FREQ:STOP %s KHz' % str(stop))  # stop frequency of display range (not useful)
                        self.gpib_inst.write('SCAN1:STAR %s KHz;*WAI' % str(start))  # entry of start frequency
                        self.gpib_inst.write('SCAN1:STOP %s KHz;*WAI' % str(stop))  # entry of stop frequency
                        self.gpib_inst.write('SCAN1:STEP 10 kHz')  # entry of step size
                        self.gpib_inst.write(':BAND:TYPE PULS')  # 6 dB??
                        self.gpib_inst.write('SCAN1:BAND:RES 10 kHz')  # entry of IF Bandwidth
                        self.gpib_inst.write('SCAN1:TIME %d ms' % self.messtime)  # measurement time
                        self.gpib_inst.write('INP:ATT:AUTO OFF')
                        self.gpib_inst.write('INP:ATT:PROT OFF')
                        self.gpib_inst.write('INP:ATT %d DB' % self.attenuation)
                        self.gpib_inst.write(
                            'SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
                        self.gpib_inst.write(
                            'SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                        self.gpib_inst.write('SCAN1:INP:ATT %d dB' % self.attenuation)  # entry of a fixed RF attenuation (0 db,10 db 50 db)
                        self.gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  # von remi
                        self.gpib_inst.write(
                            'SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                        self.gpib_inst.write(
                            'SCAN1:INP:GAIN:STAT ON')  # The preamplifier can be switched on/off separately for each subrange
                        self.gpib_inst.write('TRAC:FEED:CONT ALW')  # SCAN results available
                        self.gpib_inst.write('FORM ASC')  # specifies the data format
                        self.gpib_inst.write('FORM:DEXP:DSEP POIN')  # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
                        self.gpib_inst.write('INIT2;*WAI')  # start the scan
                        if self.mode == 'max':
                            time.sleep(5.5)
                        elif self.mode == 'average':
                            time.sleep(5.5)
                        else:
                            time.sleep(110)
                        self.gpib_inst.write(':ABOR')
                        if self.mode == 'max':
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')  # save trace1 data to PK.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"').split(";")[48:]
                            print(data_PK)
                        elif self.mode == 'average':
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\AVG.ASC"').split(";")[48:]
                        else:
                            self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC
                            data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\QPE.ASC"').split(";")[48:]
                        self.countChanged.emit(data_PK, stop)
                    else:
                        self.startfrequency = stopfre
                        print(self.startfrequency)
                        self.gpib_inst.write(':ABOR;*WAI')
                        break
                          # stop the scan
                self.count += 5
        if self.count < 5:
            for i in range (1, 30, 1):
                if (self.signal & 1) == 1:  #是奇数
                    start = i
                    stop = i + 1
                    stopfre = stop
                    self.gpib_inst.write('SCAN:RANG:COUN 1')
                    self.gpib_inst.write('FREQ:STAR %s MHz' % str(start))  # start frequency of display range
                    self.gpib_inst.write('FREQ:STOP %s MHz' % str(stop))  # stop frequency of display range (not useful)
                    self.gpib_inst.write('SCAN1:STAR %s MHz;*WAI' % str(start))  # entry of start frequency
                    self.gpib_inst.write('SCAN1:STOP %s MHz;*WAI' % str(stop))  # entry of stop frequency
                    self.gpib_inst.write('SCAN1:STEP 10 kHz')  # entry of step size
                    self.gpib_inst.write(':BAND:TYPE PULS')  # 6 dB??
                    self.gpib_inst.write('SCAN1:BAND:RES 10 kHz')  # entry of IF Bandwidth
                    self.gpib_inst.write('SCAN1:TIME %d ms' % self.messtime)  # measurement time
                    self.gpib_inst.write('INP:ATT:AUTO OFF')
                    self.gpib_inst.write('INP:ATT:PROT OFF')
                    self.gpib_inst.write('INP:ATT %d DB' % self.attenuation)
                    self.gpib_inst.write(
                        'SCAN1:INP:ATT:AUTO OFF')  # Auto Ranging off: the input attenuation setting of the scan table is used
                    self.gpib_inst.write(
                        'SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                    self.gpib_inst.write('SCAN1:INP:ATT %d dB' % self.attenuation)  # entry of a fixed RF attenuation (0 db,10 db 50 db)
                    self.gpib_inst.write('SCAN1:INP:ATT:AUTO:MODE LNO;*WAI')  # von remi
                    self.gpib_inst.write(
                        'SCAN1:INP:ATT:PROT OFF')  # This command defines whether the 0 dB position of the attenuator is to be used in manual or automatic adjustment.
                    self.gpib_inst.write(
                        'SCAN1:INP:GAIN:STAT ON')  # The preamplifier can be switched on/off separately for each subrange
                    self.gpib_inst.write('TRAC:FEED:CONT ALW')  # SCAN results available
                    self.gpib_inst.write('FORM ASC')  # specifies the data format
                    self.gpib_inst.write(
                        'FORM:DEXP:DSEP POIN')  # selects the decimal separator between ’.’ (decimal point)and ’,’ (comma)
                    self.gpib_inst.write('INIT2;*WAI')  # start the scan
                    if self.mode == 'max':
                        time.sleep(5.5)
                    elif self.mode == 'average':
                        time.sleep(5.5)
                    else:
                        time.sleep(110)
                    self.gpib_inst.write(':ABOR')
                    if self.mode == 'max':
                        self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\PK.ASC"')  # save trace1 data to PK.ASC
                        data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\PK.ASC"').split(";")[48:]
                    elif self.mode == 'average':
                        self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\AVG.ASC"')  # save trace2 data to AVG.ASC
                        data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\AVG.ASC"').split(";")[48:]
                    else:
                        self.gpib_inst.write('MMEM:STOR1:TRAC 1,"D:\Matlab_Directory\QPE.ASC"')  # save trace2 data to AVG.ASC
                        data_PK = self.gpib_inst.query('MMEM:DATA? "D:\Matlab_Directory\QPE.ASC"').split(";")[48:]
                    self.countChanged.emit(data_PK, stop)
                else:
                    self.startfrequency = stopfre
                    print(self.startfrequency)
                    self.gpib_inst.write(':ABOR;*WAI')
                    break

    def quit(self):

        print(self.signal)
        #self.gpib_inst.write(':ABOR;*WAI')
        #
        # if (self.signal & 1) == 1:  #是奇数


