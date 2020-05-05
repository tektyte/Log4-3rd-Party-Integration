# RaspberryPi

Takes in serial information from Log4 USB or POE device then
displays measurements on RaspberryPi python terminal.

## Units supported

* Current - "uA", "mA", "A"
* Voltage - "mV", "V"
* Power - "mW", "W"

## Dependencies

* pyserial

## Requirements

* Log4 USB or Log4 PoE with FW 2.x.x
* Micro-USB B to USB A-type cable
* RaspberryPi 2 or 3
* Python 2 or 3

## Setup

* Use the micro USB cable to connect Log4 device with RaspberryPi via __"MONITOR USB"__ port. 
* Make sure Log4 device is turned __ON__.
* Run the python script and the terminal should start spitting out measurement data.