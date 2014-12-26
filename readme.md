#PiNumberStation
korn101

KATYA IS LOVE KATYA IS LIFE

>**Legal Notice:**
>*The operation of an FM Transmitter, over a certain energy level , is in almost all cases, countries and local jurisdictions illegal. Check the laws of your area before operating such a device.*

**PiNumberStation** is a python/bash coded frontend that takes string messages and turns them into basic speech (preferably NATO phonetic alphabet or Combine VO) - this message is then passed over FM Radio transmission via a small antenna connected to GPIO pin 4. The hard part (modulating the sound and sending it to the antenna) is actually done by the back-end PiFM based C program.

The end result is a basic and very small FM Number Station. See: http://en.wikipedia.org/wiki/Numbers_station

#Installation:
* git clone https://github.com/korn101/PiNumberStation with SSH or Terminal
* cd PiNumberStation
* sudo nano PiNS.py
* Change desired parameters in PiNS.py:
  * repeat - whether to repeat the broadcast forever (True/False)
  * buzzer - play the buzzer (if you don't know what this is, leave it False.)
  * message - The message you want to play, all in lowercase.
* To begin transmitting message: sudo python PiNS.py

#Developer Notes:
* To push new changes: Run ./gitUpdate.sh
* To pull latest version: Run ./gitPull.sh
