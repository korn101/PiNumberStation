#PiNumberStation
###korn101

>**Legal Notice:**
>*The operation of an FM Transmitter (over a certain energy level) is in almost all countries and local jurisdictions illegal. Check the laws of your area before operating such a device.*

**PiNumberStation** is a python/bash coded frontend that takes string messages and turns them into basic speech (preferably NATO phonetic alphabet or Combine VO) - this message is then passed over FM Radio transmission via a small antenna connected to GPIO pin 4. The hard part (modulating the sound and sending it to the antenna) is actually done by the back-end PiFM based C program.

The end result is a basic and very small FM Number Station. See: http://en.wikipedia.org/wiki/Numbers_station

#Installation:
* git clone https://github.com/korn101/PiNumberStation with SSH or Terminal
* cd PiNumberStation
* sudo nano PiNS.py
* Change desired parameters in PiNS.py:
  * repeat - whether to repeat the broadcast forever (True/False)
  * buzzer_on - play the buzzer (if you don't know what this is, leave it False.)
  * message - The message you want to play, all in lowercase.
* To begin transmitting message: sudo python PiNS.py

**Important:**
Due to copyright and filesize reasons, no voice/speech files are present. Loading these files is easy.
Important to note is the files **must be 16-bit Mono WAV** files. With a file structure such that:

> The folder "vo" contains sub-folders: "misc" and "alpha".
> * where misc contains buzzer.wav
> * where alpha containts alpha.wav, bravo.wav, etc.
 
* For NATO Phonetic, I would suggest: https://www.freesound.org/people/Corsica_S/packs/14153/

#Developer Notes:
* To push new changes: Run ./gitUpdate.sh
* To pull latest version: Run ./gitPull.sh

#TODO:
* Message re-loading every loop
* Uppercase support
* Unload pifm process
* Change frequencies
* Morsecode Synthesis
