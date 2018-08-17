
#  Log4 USB and POE Serial Output

#  Takes in serial information from Log4 USB or POE device then
#  displays measurements on RaspberryPi python terminal.

#  created 2018
#  by Tekt Industries

#  This example code is in the public domain.

#  Units supported
#   Current - "uA", "mA", "A"
#   Voltage - "mV", "V"
#   Power - "mW", "W"

import serial
import time


def serialConnect(serialdevice):
    if serialdevice=='auto':
        serlocations=['/dev/ttyACM', '/dev/ttyACM0', '/dev/ttyACM1','/dev/ttyACM2', '/dev/ttyACM3','/dev/ttyACM4', '/dev/ttyACM5','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5', '/dev/ttyUSB6', '/dev/ttyUSB7', '/dev/ttyUSB8', '/dev/ttyUSB9', '/dev/ttyUSB10','/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9', 'com10', 'com11', 'com12', 'com13', 'com14', 'com15', 'com16', 'com17', 'com18', 'com19', 'com20', 'com21', 'com1', 'end']
    else:
        serlocations=[serialdevice]
    for device in serlocations:
        try:
            ser = serial.Serial(
                port=device,
                baudrate=115200,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.SEVENBITS
            )
            print device
            return ser  
        except:
            pass
    if device == 'end':
        print "No Device Found"  

class Log4USB:
    def _init_(self):
        self.current=0
        self.voltage=0
        self.power=0
        self.current_chB=0
        self.voltage_chB=0
        self.power_chB=0
        self.device=""
        self.cD=1
        self.vD=1
        self.pD=1
        self.timestamp=0
    
    def setUnits(self,currentDivision,voltageDivision,powerDivision):
        if currentDivision=='mA':
            self.cD=1000.0
        elif currentDivision=='A':
            self.cD=1000000.0
        else:
            self.cD=1
        if voltageDivision=='V':
            self.vD=1000.0
        else:
            self.vD=1
        if powerDivision=='mW':
            self.pD=1000.0
        elif powerDivision=='W':
            self.pD=1000000.0
        else:
            self.pD=1
    
    def measure(self,serialdevice):
        if (serialdevice.read())==":":
            serialdata=serialdevice.read(24).encode("hex")
            currentA=''
            voltageA=''
            powerA=''
            currentB=''
            voltageB=''
            powerB=''
            timestamp=''
            for x in range(0,16,2):
                timestamp=serialdata[6+x]+serialdata[7+x]+timestamp
            if serialdata[4]+serialdata[5]=='14':
                self.device="Log4 USB"
                for x in range(0,8,2):
                    currentA=serialdata[22+x]+serialdata[23+x]+currentA
                    voltageA=serialdata[30+x]+serialdata[31+x]+voltageA
                    powerA=serialdata[38+x]+serialdata[39+x]+powerA
            elif serialdata[4]+serialdata[5]=='20':
                self.device="Log4 PoE"
                for x in range(0,8,2):
                    currentA=serialdata[22+x]+serialdata[23+x]+currentA
                    voltageA=serialdata[30+x]+serialdata[31+x]+voltageA
                    powerA=serialdata[38+x]+serialdata[39+x]+powerA
                    currentB=serialdata[22+x]+serialdata[23+x]+currentB
                    voltageB=serialdata[30+x]+serialdata[31+x]+voltageB
                    powerB=serialdata[38+x]+serialdata[39+x]+powerB
            else:
                self.device=""
                self.current=0
                self.voltage=0
                self.power=0
                self.current_chB=0
                self.voltage_chB=0
                self.power_chB=0
            self.current=(int(currentA,16)/self.cD)
            print currentA
            self.voltage=(int(voltageA,16)/self.vD)
            self.power=(int(powerA,16)/self.pD)
            self.current_chB=(int(currentB,16)/self.cD)
            self.voltage_chB=(int(voltageB,16)/self.vD)
            self.power_chB=(int(powerB,16)/self.pD)
            self.timestamp=int(timestamp,16)/1000
        else:
            self.current=0
            self.voltage=0
            self.power=0
            self.current_chB=0
            self.voltage_chB=0
            self.power_chB=0
            self.device=""
            self.timestamp=0
        return Log4USB()


device = serialConnect('auto') 
log4usb=Log4USB()
currentUnit='mA'
voltageUnit='V'
powerUnit='mW'
log4usb.setUnits(currentUnit,voltageUnit,powerUnit)
if device:
    device.flushInput()
    while True:
        log4usb.measure(device)
        if log4usb.device=="Log4 PoE":
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log4usb.timestamp))
            print "Ch A current %f %s"  %(log4usb.current  ,  currentUnit)
            print "Ch A voltage %f %s"  %(log4usb.voltage  ,  voltageUnit)
            print "Ch A power %f %s"  %  (log4usb.power    ,  powerUnit)
            print "Ch B current %f %s"  %(log4usb.current_chB  ,  currentUnit)
            print "Ch B voltage %f %s"  %(log4usb.voltage_chB  ,  voltageUnit)
            print "Ch B power %f %s"  %  (log4usb.power_chB  ,  powerUnit)
            print ""
        elif log4usb.device=="Log4 USB":
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log4usb.timestamp))
            print "Current %f %s"  %(log4usb.current  ,  currentUnit)
            print "Voltage %f %s"  %(log4usb.voltage  ,  voltageUnit)
            print "Power %f %s"  %  (log4usb.power    ,  powerUnit)
            print ""
