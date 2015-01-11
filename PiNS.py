#!/usr/bin/python

import subprocess # for calling console
import math
import time
import wave



# Turn on buzzer:
buzzer_number = 4

monolith_on = True

# Message to synthesize and broadcast
message = "test 123"
# Would you like to repeat the message infinitely? 
repeat = True

loadFromFile = True
freq = "103.3"

# Sounds for digits/numbers.
sounds = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]


# Sounds for alphanumeric. Use NATO Phonetic
alpha = ["alpha", "bravo", "charlie", "delta",  "echo", "foxtrot", "golf", 
		"hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
		"papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor",
		"whiskey", "x-ray", "yankee", "zulu"]

def main():
	
	print("PiNumberStation started...")
	'''
	for x in range(0, len(message)):
		print(str(message[x]))
	'''

	import os.path
	if (os.path.isfile("./vo/alpha/alpha.wav") == False):
		print("Synthesis Failure: NO ALPHANUMERIC SUPPORT")
		time.sleep(5)

	return
	
def constructWavFromFile( fileName):
	fMsg = open(fileName, 'r')
	strMessage = fMsg.read()
	constructWav( strMessage )
	
	return
	
def playMessage():
	
	print("Broadcast Begin..")
	subprocess.call(["sudo", "./pifm", "./message.wav", freq])
	
	return
	
def getVO( character ):
	if character.isdigit() == True:
		return sounds[int(character)]
	else:
		if character == ',' or character == ' ':
			return "_comma.wav"
		if character == '.':
			return "_period.wav"
		if character == '\n':
			return "nova.wav"
		
		
		if character.isalpha() == True:
			return "/alpha/" + str(alpha[ord(character) - ord('a')] + ".wav")
		
	
def constructWav( strMessage ):
	
	print("Synthesizing Message..")
	
	infiles = []
	
	'''
	import audiolab, scipy
	a, fs, enc = audiolab.wavread('file1.wav')
	b, fs, enc = audiolab.wavread('file2.wav')
	c = scipy.vstack((a,b))
	audiolab.wavwrite(c, 'file3.wav', fs, enc)
	'''
	
	# determine infiles for message.
	i=0
	if buzzer_number > 0:
		j=0
		while (j < buzzer_number):
			infiles.append("./vo/misc/buzzer.wav")
			j=j+1
	else:
		infiles.append("./vo/_comma.wav")	

	infiles.append("./vo/on3.wav")

	if monolith_on == True:
		infiles.append("./vo/misc/monolith.wav")

	for character in strMessage:
		infiles.append("./vo/" + getVO(character))
		print(infiles[i+2])
		i = i + 1
		
	infiles.append("./vo/off3.wav")
	
	#infiles = ["sound_1.wav", "sound_2.wav"]
	
	outfile = "message.wav"
	
	data= []
	for infile in infiles:
	    w = wave.open(infile, 'rb')
	    data.append( [w.getparams(), w.readframes(w.getnframes())] )
	    w.close()

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	
	for x in range(0, len(infiles)):
		output.writeframes(data[x][1])
	
	#output.writeframes(data[0][1])
	#output.writeframes(data[1][1])
	#output.writeframes(data[2][1])
	output.close()
	
	print("Synthesis Complete..")
	
	return
	

# START:
main()

if (loadFromFile == False):
	constructWav(message)
else:
	constructWavFromFile("message.txt")
	
if repeat == False:
	playMessage()
else:
	while (1):
		if (loadFromFile == False):
			constructWav(message)
		else:
			constructWavFromFile("message.txt")
		
		playMessage()

#kill pifm because it doesn't kill itself, for some stupid reason.
subprocess.call(["sudo", "killall", "pifm"])
print("Done")
