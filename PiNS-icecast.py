#!/usr/bin/python
# -*- coding: utf-8 -*-
# PiNumberStation over icecast 
#
# Requires:
#
# 	- icecast 		 (https://icecast.org/download | brew install icecast)
#	- liquidsoap 	 (https://www.liquidsoap.info/doc-dev/install.html)
#	- liquidsoap-cry (liquidsoup plugin for stream to icecast)
#
# Configure:
#
# 	- 1. (required) Setup icecast: edit ```/etc/icecast.xml```, ```/usr/local/etc/icecast.xml```
#	- 2. (required) Run icecast: run ```icecast -c /usr/local/etc/icecast.xml -b```
#	- 3. (optional) Setup PiNS steaming: edit ```default.ini``` section streaming
#   - 4. (required) Setup liquidsoap config: edit ```streaming/config.liq``` with your host, and port (the same of icecast.xml)
#   - 5. (optional) Setup trasmission: edit ```streaming/stream.liq```
#
# Usage:
#
# ./PiNS-icecast.py 
#		--text your_message 
#		[--key "your_encrypt_key"] [--key-rand]
#		[-s [default]]
#
# Stream normal message:
# 	./PiNS-icecast.py --text "my message" --key "key for encrypt text with Vernam's Cipher"
#
# Stream encrypted message (use --key)
# 	./PiNS-icecast.py --text "my message" --key "key for encrypt text with Vernam's Cipher"
#
# Set trasmission config
# 	./PiNS-icecast.py --text "foo" --stream daily
# 	./PiNS-icecast.py --text "foo" --stream night
#
import sys
import subprocess # for calling console
import wave
import os.path
import ConfigParser
from random import choice
from distutils.spawn import find_executable
from string import ascii_letters
import argparse

directory=os.path.expanduser(sys.path[0])
default_trasmission=directory + "/streaming/default/main.liq"

parser = argparse.ArgumentParser(prog="PiNS-icecast.py", add_help=True, description="PiNumberStation over icecast")
parser.add_argument('--conf', '--config', '-c', metavar='config', default="default.ini", type=str, help='Config file')
parser.add_argument('--text', '--string', '-t', metavar='text', default="hello", type=str, help='text to crypt')
parser.add_argument('--key',  '--pass',   '-k', metavar='key', default="", type=str, help='Encrypt text with VernamCipher')
parser.add_argument('--key-rand',  '--pass-rand',  metavar='key_random', const=True, nargs='?', default=False, type=bool, help='Encrypt text with VernamCipher')
parser.add_argument('--stream', '--trasmission', '-s', metavar="stream", type=str, default=default_trasmission, help="Your stream name")

"""Get abs path"""
def resolve_path(path):
	path = os.path.expanduser(path)
	if os.path.isabs(path):
		pass
	else:
		path = directory +"/"+ path

	return path


class PiNumberStationConfig:

	config = ConfigParser.ConfigParser()
	args   = {}

	sound  = ["zero.wav", "one.wav", "two.wav", "three.wav", "four.wav", "five.wav", "six.wav", "seven.wav", "eight.wav", "nine.wav"]
	alpha  = [
		"alpha", "bravo", "charlie", "delta",  "echo", "foxtrot", "golf",
		"hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
		"papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor",
		"whiskey", "x-ray", "yankee", "zulu"
	]

	def __init__(self, *args):
		self.args = args

	def loadConfig(self, configFile):
		if not os.path.exists(configFile):
			raise Exception("❌	config %s not exists", configFile)

		self.config.read(configFile)

	"""Encrypt text"""
	def encrypt(self, text, key=None):
		response = {"text": text, "key": key, "encrypt": None}

		if key:
			process = subprocess.Popen([sys.path[0] + "/encoder.py", "--enc-text", args.text, "--enc-key", args.key], stdout=subprocess.PIPE)
			result = process.stdout.readlines()[-1]
			response["encrypt"] = result.rstrip()

		return response

	"""Vocal message from text"""
	def constructWav(self, message, pwd=None):
		message    = self.encrypt(message, pwd)
		strMessage = message["encrypt"]

		if not strMessage:
			raise Exception("❌ Empty message (use --text string)")

		print(">> Synthesizing Message.. [key=%s]" % (args.key))

		infiles       = []
		strMessageOut = strMessage

		# determine infiles for message.

		for file in self.config.get('streaming', 'prepend').split(","):
			if not file[0] == "/" or not file[0] == ".":
				file = sys.path[0] + "/" + file

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
				file = sys.path[0] + "/" + file

			if os.path.exists(file):
				infiles.append(file)
			else:
				print  "File %s not exists ... skipped!" % file

			infiles.append(file)

		infiles.append(sys.path[0] + "/vo/off3.wav")

		data = []
		for infile in infiles:
		    w = wave.open(infile, 'rb')
		    data.append( [w.getparams(), w.readframes(w.getnframes())] )
		    w.close()


		if os.path.isabs(args.stream):
			outprefix = os.path.dirname(args.stream)
		else:
			outprefix = directory + "/streaming/" + os.path.dirname(args.stream)

		outfile = outprefix + "/message.wav"
		if not os.path.exists(outfile):
			f=open(outfile, 'w+')
			f.write("")
			f.close()
			
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


		stream_cfg  = os.path.abspath(os.path.expanduser(args.stream))
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

if __name__ == "__main__":
	args = parser.parse_args()

	args.stream = os.path.expanduser(args.stream if args.stream.endswith('.liq') else args.stream + "/main.liq")
	if not os.path.isabs(args.stream):
		args.stream = "streaming/%s" % args.stream

	# random key from text len
	args.key    = "".join([choice(ascii_letters).lower() for char in args.text]) if args.key_rand else args.key

	# expand path's
	for key in ['conf', 'stream']:
		try:
			value = getattr(args, key)
			setattr(args, key, resolve_path(value))
		except e:
			pass

	# run PiNS
	NStation = PiNumberStationConfig(vars(args))
	NStation.loadConfig(args.conf)
	NStation.constructWav(args.text, args.key)
	NStation.stream_message()