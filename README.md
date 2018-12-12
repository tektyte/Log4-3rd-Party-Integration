# Log4 3rd Party Integration
This is the repository for 3rd Party Integration for Log4 Devices.

## Device Supported
 * [Log4.USB](https://www.tektyte.com/log4usb.html)  
 * [Log4.PoE](https://www.tektyte.com/log4poe.html) 

## 3rd Party Integration
### Arduino
Log4 USB and POE Serial Output

 Takes in serial information from Log4 USB or POE device then
 displays measurements on Arduino Serial Monitor.

### RaspberryPi
Takes in serial information from Log4 USB or POE device then
displays measurements on RaspberryPi python terminal.

#### Units supported

 * Current - "uA", "mA", "A"
 * Voltage - "mV", "V"
 * Power - "mW", "W"

#### Dependencies
 * pyserial

## Log4 Serial Communication Protocol
In order to understand more about the general protocol followed by Log4 Devices for communication over Serial connection, __[click here](docs/Tektyte-Log4-Serial-Communications-Protocol.pdf)__.