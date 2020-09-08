import numpy as np

def decode(cipher, n):
	return list(map(lambda x: x ^ n, cipher))	

def get_length(cipher):
	length_bag = np.array([0.] * 14)

	for n in range(1, 14):
		frequency_bag = np.array([0] * 256)
		stream = cipher[::n]

		for c in stream:
			frequency_bag[c] += 1

		length_bag[n] = np.sum((frequency_bag / len(stream)) ** 2)

	return np.argmax(length_bag)


def get_key(cipher, length):	
	key = []

	for i in range(length):
		stream = cipher[i::length]
		shift_bag = np.array([0.] * 256)

		for shift in range(256):
			invalid_message_space = False
			frequency_bag = np.array([0] * 27)

			for c in decode(stream, shift):
				if c < 32 or c > 126:
					invalid_message_space = True
					break
				
				if c >= 97 and c <= 122:
					frequency_bag[c - 97] += 1
				elif c == 32:
					frequency_bag[26] += 1

			if invalid_message_space:
				continue

			shift_bag[shift] = np.sum((frequency_bag / len(stream)) ** 2)

		key.append(np.argmax(shift_bag))

	return key

def main():
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