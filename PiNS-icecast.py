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
#		[--key "your_encrypt_key"] 
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

import argparse
default_trasmission=sys.path[0] + "/streaming/default/main.liq"

parser = argparse.ArgumentParser(prog="PiNS-icecast.py", add_help=True, description='Encrypt text with VernamCipher')
parser.add_argument('--conf', '--config', '-c', metavar='config', default="default.ini", type=str, help='Config file')
parser.add_argument('--text', '--string', '-t', metavar='text', default="hello", type=str, help='text to crypt')
parser.add_argument('--key',  '--pass',   '-k', metavar='key', default="", type=str, help='Encrypt text with VernamCipher')
parser.add_argument('--stream', '--trasmission', '-s', metavar="stream", type=str, default=default_trasmission, help="Your stream name")
args = parser.parse_args()
args.stream = args.stream if args.stream.endswith('.liq') else args.stream + "/main.liq"


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
	print(">> Synthesizing Message..")

	infiles       = []
	strMessageOut = strMessage
	dest          = os.path.dirname(args.stream)

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
		print "\t %s => %s" % (character, getVO(character))

	for file in config.get('streaming', 'append').split(","):
		if not file[0] == "/" or not file[0] == ".":
			file = sys.path[0] + "/" + file

		if os.path.exists(file):
			infiles.append(file)
		else:
			print  "File %s not exists ... skipped!" % file

		infiles.append(file)

	infiles.append(sys.path[0] + "/vo/off3.wav")

	outfile = dest + "/message.wav"
	data    = []

	for infile in infiles:
	    w = wave.open(infile, 'rb')
	    data.append( [w.getparams(), w.readframes(w.getnframes())] )
	    w.close()

	if not os.path.exists(outfile):
		f.open(outfile, 'w+')
		f.close()
		
	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])

	for x in range(0, len(infiles)):
		output.writeframes(data[x][1])

	output.close()
	print("<< Synthesis Complete..")

	return

"""Run LiquidSoap"""
def stream_message():
	liquidsoap_bin = config.get('streaming', 'liquidsoap_bin').replace('"', '').strip()
	liquidsoap_bin = os.path.expanduser(liquidsoap_bin)

	if not find_executable(liquidsoap_bin):
		raise Exception("❌	%s not exists... edit your .ini (key streaming.liquidsoap_bin)" % liquidsoap_bin)


	stream_cfg = args.stream
	if not os.path.isabs(args.stream):
		stream_cfg  = os.path.dirname(__file__) + "/streaming/" + args.stream

	stream_cfg  = os.path.abspath(os.path.expanduser(stream_cfg))
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

if __name__ == "__main__":
	if not os.path.exists(args.conf):
		raise Exception("❌	config %s not exists", args.conf)

	config.read(args.conf)

	if len(args.key) > 0:
		process=subprocess.Popen([sys.path[0] + "/encoder.py", "--enc-text", args.text, "--enc-key", args.key], stdout=subprocess.PIPE)
		result=process.stdout.readlines()[-1]
		print(result)
		message=result.rstrip()
	else:
		message=args.text


	if not message:
		raise Exception("❌ Empty message (use --text string)")

	constructWav(message)
	stream_message()

