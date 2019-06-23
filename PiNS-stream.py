#!/usr/bin/python
import sys
import subprocess # for calling console
import wave
import os.path
import ConfigParser
from random import choice

config = ConfigParser.ConfigParser()
# Sounds for digits/numbers.
sounds = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]

# Sounds for alphanumeric. Use NATO Phonetic
alpha = [
	"alpha", "bravo", "charlie", "delta",  "echo", "foxtrot", "golf",
	"hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
	"papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor",
	"whiskey", "x-ray", "yankee", "zulu"
]

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
	strMessageOut = strMessage


	# determine infiles for message.

	for file in config.get('streaming', 'prepend').split(","):
		if not file[0] == "/" or not file[0] == ".":
			file = sys.path[0] + "/" + file

		if os.path.exists(file):
			infiles.append(file)
		else:
			print  "File %s not exists ... skipped!" % file

	for character in strMessageOut:
		char_sound = sys.path[0] + "/vo/" + getVO(character)
		infiles.append(char_sound)
		print char_sound

	for file in config.get('streaming', 'append').split(","):
		if not file[0] == "/" or not file[0] == ".":
			file = sys.path[0] + "/" + file

		if os.path.exists(file):
			infiles.append(file)
		else:
			print  "File %s not exists ... skipped!" % file

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


def vernam(key,message):
    message = str(message)
    m = message.upper().replace(" ","") # Convert to upper case, remove whitespace
    encrypt = []

    try:
        key = int(key)           # if the key value is not a number, then run with key = 0
    except ValueError:
        key = 0
    for i in range(len(m)):
        letter = ord(m[i])-65      # Letters now range 0-25
        letter = (letter + key)%25 # Alphanumeric + key mod 25 = 0-25
        letter +=65
        

        encrypt.append(str(letter)) #chr(letter) # Concatenate message
        
    return "".join(encrypt)

def main():
	configFile = "default.ini"
	if (len(sys.argv) > 1):
		# if arguments present
		configFile = sys.argv[1]

		if not configFile.endswith(".ini"):
			configFile = configFile + ".ini"

	config.read(configFile)

	bin=config.get('streaming', 'binary')

	#message=open("message.txt").read()
	message=raw_input("Digita il messaggio\n")
	enc_key=raw_input("Digita la chiave di crittografia o premi invio per una generata automaticamente\n")
	if not enc_key:
		for char in message:
			enc_key=choice(range(0, 25))

	# see https://repl.it/@GeorgeHill1/Vernam-Cipher
	enc_message=vernam(enc_key, message)
	print(enc_message)

	constructWav(enc_message)
	subprocess.call([sys.path[0] + "/streaming/stream.liq"]);

main()