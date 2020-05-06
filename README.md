# Log4 3rd Party Integration
This is the repository for 3rd Party Integration for Log4 Devices.

## Device Supported
 * [Log4.USB](https://www.tektyte.com/log4usb.html)  
 * [Log4.PoE](https://www.tektyte.com/log4poe.html) 

## Firmware Version
Log4 Devices with legacy firmware (FW 1.x.x) should check __[here](V1.x.x)__ and for latest firmware should check here __[here](V2.x.x)__ 

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
Log4 Devices follows specific serial protocols depending on their firmware. Checkout the firmware specific serial protocol below -
* __[Serial Protocol V2.0 for latest FW 2.x.x](docs/Tektyte-Log4-Serial-Communications-Protocol-v2.0.pdf)__
* __[Serial Protocol V1.0 for legacy FW 1.x.x](docs/Tektyte-Log4-Serial-Communications-Protocol-v1.0.pdf)__
