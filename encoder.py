#!/usr/bin/python
import sys
import argparse

parser = argparse.ArgumentParser(prog="enc", add_help=True, description='Encrypt text with VernamCipher')

parser.add_argument('--enc-text', '-s', metavar='enc_text', default="hello", type=str, help='text to crypt')
parser.add_argument('--enc-key', '-k', metavar='enc_key', default="olleh", type=str, help='Encrypt key (should be the same lenght of text)')

args = parser.parse_args()


class VernamCipher:

	def __init__(self, key):
		self.characters = "/ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		self.chars = list(self.characters)
		self.key = key.upper()

	def __charIndex(self, char):
		index = self.characters.find(char)

		if index < 0:
			raise Exception("Char not allowed")

		return index

	"""Encode message with self.key"""
	def encode(self, message):
		enc     = []
		message = message.upper()

		# verificare message > key
		if len(message) > len(key):
			raise Exception("Key < message")

		pos = -1
		for char in message:
			pos += 1

			try:
				num_1 = self.__charIndex(char)
				num_2 = self.__charIndex(self.key[pos])
			except Exception as e:
				num_1 = 0
				num_2 = 0
				pass

			char_sum = ( num_1 + num_2 ) % len(self.characters)
			enc.append(char_sum)

		return enc

if __name__ == "__main__":
	message = args.enc_text if args.enc_text else raw_input("Write your message (only alpha-numerics): \n").upper()
	key     = args.enc_key  if args.enc_key  else raw_input("Write encrypt key (key >= message_len): \n").upper()

	if key == "!":
		key = ""
		for char in message:
			key=key + str(choice(range(0, 25)))

	cipher = VernamCipher(key)
	text   = cipher.encode(message)
	str    = "".join( [str(char) for char in text])

	print("Key = %s", key)
	
	sys.stdout.write( str + "\n" )
	sys.exit(0)
