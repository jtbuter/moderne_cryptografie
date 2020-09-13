key = [196, 11, 107, 83, 41, 229]

KEY_LENGTH = len(key)

cipher = bytes.fromhex(open('ciphertext.txt', 'r').readline())
plain = ''

for i, c in enumerate(cipher):
	plain += chr(255 ^ (c ^ key[i % KEY_LENGTH]))

print(plain)