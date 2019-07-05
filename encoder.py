#!/usr/bin/python
import sys
import argparse
from string import ascii_letters
from random import choice

import pprint
try:
	from itertools import zip_longest
except Exception as e:
	from itertools import izip_longest as zip_longest

parser = argparse.ArgumentParser(prog="enc", add_help=True, description='Encrypt text with VernamCipher')

parser.add_argument('--method', default="encrypt", type=str)
parser.add_argument('--text', '-s', metavar='text', default="hello", type=str, help="Message to encrypt/decrypt")
parser.add_argument('--key',  '-k', metavar='key', default="", type=str, help="Encrypt/Decrypt key")


class VernamCipher:
	alphabet = list("abcdefghijklmnopqrstuvwxyz !,.")

	def chunk(self, str, size):
		seq = list(str)
		x   = [iter(seq)] * size
		l   = zip_longest(*x, fillvalue='0')
		return [''.join(tups) for tups in l] 


	def encrypt(self, st, key):
		if len(st) != len(key):
			return "Text and Key have to be the same length."

		nText    = []
		kText    = []

		for i in range(len(st)):
			nText.append(self.alphabet.index(st[i].lower()))
			kText.append(self.alphabet.index(key[i].lower()))

		res = {"encode":"", "indexs":""}
		for i in range(len(nText)):
			index = (nText[i] + kText[i]) % len(self.alphabet)
			res["encode"] += self.alphabet[index]
			res["indexs"] += str(index)

		return res;

	def decrypt(self, st, key):
		if len(st) != len(key):
			return "Text and Key have to be the same length."

		alphabet = list("abcdefghijklmnopqrstuvwxyz")
		nText = []
		kText = []

		for i in range(len(st)):
			nText.append(self.alphabet.index(st[i].lower()))
			kText.append(self.alphabet.index(key[i].lower()))
		out = ""
		for i in range(len(nText)):
			op = (nText[i] - kText[i])
			if op < 0:
				x = len(self.alphabet) + op
			else:
				x = op % len(self.alphabet)
			out += alphabet[x]
		return out;



if __name__ == "__main__":
	args = parser.parse_args()

	args.key = "".join([choice(ascii_letters).lower() for char in args.text]) if len(args.key) < 1 else args.key

	if len(args.key) < len(args.text):
		raise Exception("Error: key MUST be same length of text")

	cipher = VernamCipher()

	if (args.method == "encrypt"):		
		res  = cipher.encrypt(args.text, args.key)
		text = " ".join(cipher.chunk(res["indexs"], 5))
	else:
		text = cipher.decrypt(args.text, args.key)

	print("key = %s" % args.key)
	
	sys.stdout.write( text + "\n" )
	sys.exit(0)