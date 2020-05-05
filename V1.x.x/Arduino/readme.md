# Arduino

 Takes in serial information from __Log4 USB__ or __POE__ device then
 displays measurements on Arduino Serial Monitor.

## Requirements

* Log4 USB or Log4 PoE
* Arduino Mega 2560
* 4 Male-Male jumper cables
* Serial Monitor

## Setup

![Log4 serial pin configuration](https://github.com/tektyte/Log4-3rd-Party-Integration/raw/master/Arduino/Log4SerialConnection.png "Log4 Serial pin configuration")

* Connect Arduino to the PC via a USB cable.
* Connect Arduino __5V__ pin or __3.3V__ pin (depending on logic level of Arduino) to the Log4 VCC pin.
* Connect Arduino GND pin to the Log4 GND pin.
* Connect Arduino Tx pin to Log4 Rx pin.
* Connect Arduino Rx pin to Log4 Tx pin.
* Open Serial Monitor on PC and it should start spitting out measurement data.
