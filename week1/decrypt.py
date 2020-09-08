import numpy as np

MAX_KEY = 14

def get_length(cipher):
	# For keeping track of 'distributions', [0] is always empty,
	# but slightly easier for programming
	lengths = np.array([0.] * MAX_KEY)

	# Iterate possible key lengths
	for n in range(1, MAX_KEY):
		# Tracking frequency of bytes
		frequency_bag = np.array([0] * 256)
		# Get every nth character, starting at 0
		stream = cipher[::n]

		for c in stream:
			frequency_bag[c] += 1

		# Summation of frequencies squared
		lengths[n] = np.sum((frequency_bag / len(stream)) ** 2)

	# Small values represent uniformly distributed frequencies,
	# largest value is likely permutation of plaintext.
	return np.argmax(lengths)


def get_key(cipher, length):
	# Initialize key with only 0000 0000's.	
	key = [0] * length

	# Iterate all key positions
	for i in range(length):
		# Initalize ith stream.
		stream = cipher[i::length]
		# For keeping track of 'distributions'
		shift_bag = np.array([0.] * 256)

		# Iterate possible bytes
		for shift in range(256):
			invalid_message_space = False
			# Tracking frequency of a-z and ' '
			frequency_bag = np.array([0] * 27)

			# Encodes/decodes cipher by XORing with some byte shift.
			for c in map(lambda x: x ^ shift, stream):
				if c < 32 or c > 126:
					invalid_message_space = True
					break
				
				# Save a-z and ' '
				if c >= 97 and c <= 122:
					frequency_bag[c - 97] += 1
				elif c == 32:
					frequency_bag[26] += 1

			if invalid_message_space:
				continue

			# Summation of frequencies squared
			shift_bag[shift] = np.sum((frequency_bag / len(stream)) ** 2)

		# Small values represent uniformly distributed frequencies,
		# largest value is likely original plaintext.
		key[i] = np.argmax(shift_bag)

	return key

def main():
	# Conver hex from first line to bytes.
	with open("ciphertext.txt", "r") as f:
		cipher = bytes.fromhex(f.readline())

	key_length = get_length(cipher)
	key = get_key(cipher, key_length)
	
	message = ""
	pos = 0

	for c in cipher:
		message += chr(c ^ key[pos % key_length])
		pos += 1
	
	print(message)

if __name__ == "__main__":
	main()