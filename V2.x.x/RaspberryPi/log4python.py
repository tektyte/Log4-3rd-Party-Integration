#  Log4 USB and POE Serial Output

#  Takes in serial information from Log4 USB or POE device then
#  displays measurements on RaspberryPi python terminal.
#  Cancel the streaming by using Ctrl+C while program is running.

#  created 2018
#  by Tekt Industries

#  This example code is in the public domain.

#  Units supported
#   Current - "uA", "mA", "A"
#   Voltage - "mV", "V"
#   Power - "mW", "W"
from __future__ import print_function

import serial
import struct
import datetime
import time

SLAVE_CMD = 11

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
            )
            print(device)
            return ser  
        except:
            pass
    if device == 'end':
        print("No Device Found")
		
class Log4Device:
    PROTOCOL_HEADER_STRUCT = struct.Struct("<BBB")
    SET_STREAM_CMD_STRUCT = struct.Struct("<BBBBBB")
    SLAVE_DATA_USB_STRUCT = struct.Struct("<QHii")
    SLAVE_DATA_POE_STRUCT = struct.Struct("<QHiiii")

    def __init__(self):
        self.current=0.0
        self.voltage=0.0
        self.power=0.0
        self.current_chB=0.0
        self.voltage_chB=0.0
        self.power_chB=0.0
        self.device=""
        self.cD=1.0
        self.vD=1.0
        self.pD=1.0
        self.timestamp=0
    
    def setUnits(self,currentDivision,voltageDivision):
        if currentDivision=='mA':
            self.cD=1000.0
        elif currentDivision=='A':
            self.cD=1000000.0
        else:
            self.cD=1.0
        if voltageDivision=='V':
            self.vD=1000.0
        else:
            self.vD=1.0

    def setStreaming(self, serialdevice, streaming):
        serialdevice.write(Log4Device.SET_STREAM_CMD_STRUCT.pack(0x3A, 0x01, 0x11, 0x01, 0x01 if streaming else 0x00, 0x0A))

    def measure(self, serialdevice):
        byte_read = serialdevice.read()
        if byte_read == b":":
            serialdata=serialdevice.read(3)
            (address, command_code, data_len) = Log4Device.PROTOCOL_HEADER_STRUCT.unpack(serialdata)
            data = serialdevice.read(data_len)
            end_byte = serialdevice.read()
            if end_byte != b'\n':
                return

            if command_code == SLAVE_CMD:
                currentA = 0
                voltageA = 0
                currentB = 0
                voltageB = 0
                timestamp = 0
                timestamp_us = 0

                if data_len == 18:
                    self.device = "Log4 USB"
                    timestamp, timestamp_us, currentA, voltageA = Log4Device.SLAVE_DATA_USB_STRUCT.unpack(data)
                elif data_len == 26:
                    self.device = "Log4 PoE"
                    timestamp, timestamp_us, currentA, voltageA, currentB, voltageB = Log4Device.SLAVE_DATA_POE_STRUCT.unpack(data)

                self.current = currentA / self.cD
                self.voltage = voltageA / self.vD
                self.power = self.current * self.voltage
                self.current_chB = currentB / self.cD
                self.voltage_chB = voltageB / self.vD
                self.power_chB = self.current_chB * self.voltage_chB
                self.timestamp = (timestamp / 1.0e3) + (timestamp_us / 1.0e6)

if __name__ == '__main__':

    device = serialConnect('auto')
    log4usb=Log4Device()
    currentUnit='mA'
    voltageUnit='V'
    powerUnit='mW' # note the power unit is dependent on the current and voltage units specified
    log4usb.setUnits(currentUnit,voltageUnit)
    if device:
        device.flushInput()
        log4usb.setStreaming(device, True)
        try:
            while True:
                log4usb.measure(device)
                if log4usb.device == "Log4 PoE":
                    print(datetime.datetime.fromtimestamp(log4usb.timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"))
                    print("Ch A current %f %s"  %(log4usb.current  ,  currentUnit))
                    print("Ch A voltage %f %s"  %(log4usb.voltage  ,  voltageUnit))
                    print("Ch A power %f %s"  %  (log4usb.power    ,  powerUnit))
                    print("Ch B current %f %s"  %(log4usb.current_chB  ,  currentUnit))
                    print("Ch B voltage %f %s"  %(log4usb.voltage_chB  ,  voltageUnit))
                    print("Ch B power %f %s"  %  (log4usb.power_chB  ,  powerUnit))
                    print("")
                elif log4usb.device == "Log4 USB":
                    print(datetime.datetime.fromtimestamp(log4usb.timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"))
                    print("Current %f %s"  %(log4usb.current  ,  currentUnit))
                    print("Voltage %f %s"  %(log4usb.voltage  ,  voltageUnit))
                    print("Power %f %s"  %  (log4usb.power    ,  powerUnit))
                    print("")
        except KeyboardInterrupt:
            log4usb.setStreaming(device, False)
