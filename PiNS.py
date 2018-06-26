#!/usr/bin/python

import subprocess # for calling console
import math
import time
import wave
import sys
import random
import ConfigParser


configFile = "default.ini"
if (len(sys.argv) > 1):
	# if arguments present
	configFile = sys.argv[1]

	if not configFile.endswith(".ini"):
		configFile = configFile + ".ini"

config = ConfigParser.ConfigParser()
config.read(configFile)


buzzer_number                 = config.getint('buzzer', 'times')
monolith_on                   = config.getboolean('monolith', 'enabled')
transmitter_binary            = config.get('transmitter', 'binary')
repeat                        = True
repeat_infinite               = config.getboolean('repeat', 'infinite')
repeat_counter                = config.getint('repeat', 'exit_after')
repeat_interval_break_seconds = config.getint('repeat', 'delay')
freq                          = config.get('general', 'freq')

audio_prepend                 = config.get('audio', 'prepend')
audio_append                  = config.get('audio', 'append')


# Give the pifm extension executable rights.
subprocess.call(["sudo", "chmod", "+x", transmitter_binary])

# Message to synthesize and broadcast
message = "123456789 abcdefghijklmnopqrstuvwxyz"
loadFromFile = True

# Sounds for digits/numbers.
sounds = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]


# Sounds for alphanumeric. Use NATO Phonetic
alpha = ["alpha", "bravo", "charlie", "delta",  "echo", "foxtrot", "golf",
		"hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
		"papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor",
		"whiskey", "x-ray", "yankee", "zulu"]


def main():

	print("PiNumberStation started...")
	print("Broadcast on " + str(freq))
	'''
	for x in range(0, len(message)):
		print(str(message[x]))
	'''

	import os.path
	if (os.path.isfile(sys.path[0] + "/vo/alpha/alpha.wav") == False):
		print("Synthesis Failure: NO ALPHANUMERIC SUPPORT")
		time.sleep(5)

	return

def constructWavFromFile( fileName):
	fMsg = open(sys.path[0] + "/" + fileName, 'r')
	strMessage = fMsg.read()
	constructWav( strMessage )

	return

def playMessage():

	print("Broadcast Begin..")

	if transmitter_binary == "pifm":
		subprocess.call(["sudo", sys.path[0] + "/pifm", sys.path[0] + "/message.wav", freq])
	else:
		subprocess.call(["sudo", sys.path[0] + "/" + transmitter_binary, "-f", freq, sys.path[0] + "/message.wav"])

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

	#if enable_encryption == True:
	#	strMessageOut = encrypt(strMessage, encKey)
	#else:
	#	strMessageOut = strMessage

	strMessageOut = strMessage

	'''
	import audiolab, scipy
	a, fs, enc = audiolab.wavread('file1.wav')
	b, fs, enc = audiolab.wavread('file2.wav')
	c = scipy.vstack((a,b))
	audiolab.wavwrite(c, 'file3.wav', fs, enc)
	'''

	# determine infiles for message.
	i=0
	for file in audio_prepend.split(","):
		if not file[0] == "/" or not file[0] == ".":
			file = sys.path[0] + "/" + file
		infiles.append(file)

	for character in strMessageOut:
		infiles.append(sys.path[0] + "/vo/" + getVO(character))
		print(infiles[i+2])
		i = i + 1


	for file in audio_append.split(","):
		if not file[0] == "/" or not file[0] == ".":
			file = sys.path[0] + "/" + file
		infiles.append(file)

	infiles.append(sys.path[0] + "/vo/off3.wav")

	outfile = sys.path[0] + "/message.wav"
	data    = []

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

while (True):
	if (loadFromFile == False):
		constructWav(message)
	else:
		constructWavFromFile("message.txt")

	print "Construction Complete.."

	print "Playing ..."
	playMessage()

	if not repeat_infinite:
		repeat_counter -= 1

		if repeat_counter <= 0:
			break

	if repeat_interval_break_seconds > 0:
		print "Sleep ", repeat_interval_break_seconds, " secs ..."
		time.sleep(repeat_interval_break_seconds)

#kill pifm because it doesn't kill itself, for some stupid reason.
subprocess.call(["sudo", "killall", transmitter_binary])
print("Done")

