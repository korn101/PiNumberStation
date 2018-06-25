#!/usr/bin/python

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

# main
message = raw_input("Write your message (only alpha-numerics): \n").upper()
key     = raw_input("Write encrypt key (key >= message_len): \n").upper()

cipher = VernamCipher(key)
text   = cipher.encode(message)
print text

confirm = raw_input("Save to message.txt? [Y/N]\n").lower()
if confirm == "y":
	try:
		fd = open("message.txt", "w+")
		fd.writelines(" ".join( [str(char) for char in text]) )
		fd.close()
		print "message.txt updated"
	except Exception as e:
		print e
		pass