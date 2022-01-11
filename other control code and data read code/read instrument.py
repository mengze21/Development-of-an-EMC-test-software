import pyvisa

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
#print(SignalGenerator.query('*IDN?'))
print(HpSwitch.query('ID?'))

'''# HP switch
HpSwitch.write('OLAP 0')
HpSwitch.write('CLOSE 101')
HpSwitch.write('CLOSE 102')
HpSwitch.write('CLOSE 103')
HpSwitch.write('OPEN 101')
#HpSwitch.write('OPEN 102')
#HpSwitch.write('OPEN 103')
HpSwitch.write('CMON 1')'''

# Power Meter
PowerMeter.write('*RST')
PowerMeter.write('INP:NSEL 1')
PowerMeter.write('SENS1:POW:UNIT DBM')
PowerMeter.write('POW:ATT 50')
PowerMeter.write('CORR:FREF 80 MHz; STATE ON')
print(PowerMeter.query('MEAS?'))
PowerMeter.write('*RST')
PowerMeter.write('INP:NSEL 2')
PowerMeter.write('SENS2:POW:UNIT DBM')
PowerMeter.write('POW:ATT 50')
PowerMeter.write('CORR:FREF 80 MHz; STATE ON')
print(PowerMeter.query('MEAS?'))

'''# Signal generator
SignalGenerator.write('*RST')
SignalGenerator.write(':OUTP OFF')
SignalGenerator.write('MOD:STAT OFF')
SignalGenerator.write(':SOURCE:FREQUENCY:CW 80 Mhz') # RS: FR 80 MZ  Sets the frequency of the RF output signal.
SignalGenerator.write(':POWER -37 dBm')            # RS: AP -37 DM'''






