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
import os.path
import sys
import argparse
import numbers_station 
from random import choice
from string import ascii_letters

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
	config = vars(args)
	NStation = numbers_station.PiNumberStation(**config)
	NStation.constructWav(args.text, args.key)
	NStation.stream_message()