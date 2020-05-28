# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess # for calling console
import wave
import ConfigParser
from distutils.spawn import find_executable

directory=os.path.expanduser(sys.path[0])

"""Get abs path"""
def resolve_path(path):
	path = os.path.expanduser(path)
	if os.path.isabs(path):
		pass
	else:
		path = directory +"/"+ path

	return path


class PiNumberStation:

	config = ConfigParser.ConfigParser()
	args   = {}

	sound  = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]
	alpha  = [
		"alpha", "bravo", "charlie", "delta",  "echo", "foxtrot", "golf",
		"hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
		"papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor",
		"whiskey", "x-ray", "yankee", "zulu"
	]

	def __init__(self, **args):
		self.args = args
		self.loadConfig(args['conf'])

	def loadConfig(self, configFile):
		if not os.path.exists(configFile):
			raise Exception("❌	config %s not exists", configFile)

		self.config.read(configFile)

	"""Encrypt text"""
	def encrypt(self, text, key=None):
		response = {"_text": text, "text": text, "key": key}

		if key:
			process = subprocess.Popen([
					directory + "/encoder.py", 
					"--method", "encrypt",
					"--text", text, 
					"--key", key
				],
				stdout=subprocess.PIPE
			)
			stdout_lines = process.stdout.readlines()
			result = stdout_lines[-1]
			response["text"] = result.rstrip()

		return response

	"""Vocal message from text"""
	def constructWav(self, text, key=None):
		message    = self.encrypt(text, key)
		strMessage = message["text"]

		if not strMessage:
			raise Exception("❌ Empty message (use --text string)")

		# create wav file to streaming directory (if not exists)
		if os.path.isabs(self.args['stream']):
			outprefix = os.path.dirname(self.args['stream'])
		else:
			outprefix = directory + "/streaming/" + os.path.dirname(self.args['stream'])

		outfile = outprefix + "/message.wav"
		if not os.path.exists(outfile):
			f=open(outfile, 'w+')
			f.write("")
			f.close()

		print(">> Synthesizing Message to %s" %(outfile))
		print("\t Message: %s\n\t     Key: %s\n\n" %(text, key))

		infiles       = []
		strMessageOut = strMessage

		# determine infiles for message.

		for file in self.config.get('streaming', 'prepend').split(","):
			if not file[0] == "/" or not file[0] == ".":
				file = directory + "/" + file

			if os.path.exists(file):
				infiles.append(file)
			else:
				print  "File %s not exists ... skipped!" % file

		for character in strMessageOut:
			charSound  = self.getVO(character)
			char_sound = directory + "/vo/" + charSound
			infiles.append(char_sound)

			print "\t %s => %s" % (character, charSound)

		for file in self.config.get('streaming', 'append').split(","):
			if not file[0] == "/" or not file[0] == ".":
				file = directory + "/" + file

			if os.path.exists(file):
				infiles.append(file)
			else:
				print  "File %s not exists ... skipped!" % file

			infiles.append(file)

		infiles.append(directory + "/vo/off3.wav")

		data = []
		for infile in infiles:
		    w = wave.open(infile, 'rb')
		    data.append( [w.getparams(), w.readframes(w.getnframes())] )
		    w.close()

			
		output = wave.open(outfile, 'wb')
		output.setparams(data[0][0])

		for x in range(0, len(infiles)):
			output.writeframes(data[x][1])

		output.close()
		print("<< Synthesis Complete..")

		return

	"""Sound from text"""
	def getVO(self, character):
		if character.isdigit() == True:
			return self.sound[int(character)]
		else:
			if character == ',' or character == ' ':
				return "_comma.wav"
			if character == '.':
				return "_period.wav"
			if character == '\n':
				return "nova.wav"

			if character.isalpha() == True:
				return "/alpha/" + str(self.alpha[ord(character) - ord('a')] + ".wav")

	"""Run LiquidSoap"""
	def stream_message(self):
		liquidsoap_bin = self.config.get('streaming', 'liquidsoap_bin').replace('"', '').strip()
		liquidsoap_bin = os.path.expanduser(liquidsoap_bin)

		if not find_executable(liquidsoap_bin):
			raise Exception("❌	%s not exists... edit your .ini (key streaming.liquidsoap_bin)" % liquidsoap_bin)


		stream_cfg  = os.path.abspath(os.path.expanduser(self.args['stream']))
		stream_file = os.path.basename(stream_cfg)
		stream_dir  = os.path.dirname(stream_cfg)


		if not os.path.exists(stream_dir):
			print "ℹ️	Copy default config with:"
			print "		mkdir -p %s" % (stream_dir)
			raise Exception("❌	Directory %s not exists" % (stream_dir))

		if not os.path.exists(stream_cfg):
			print "ℹ️	Copy main config with:"
			print "		cp %s %s/main.liq" % ( sys.path[0] + "/streaming/default/main.liq", stream_dir)
			raise Exception("❌	%s not founded..." % (stream_file))

		print("Starting process: %s %s" % (liquidsoap_bin, stream_cfg))
		subprocess.call([liquidsoap_bin, stream_cfg])

	def get_stream(self):
		return os.path.dirname(args.stream).split("/")[-1]