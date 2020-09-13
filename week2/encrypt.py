import random

KEY_LENGTH = 6

key = random.sample(range(256), KEY_LENGTH)
plain = "".join(open('message.txt', 'r').read().splitlines())
cipher = ''

for i, c in enumerate(plain):
	cipher += '{0:02x}'.format(255 ^ (ord(c) ^ key[i % KEY_LENGTH]))

with open('ciphertext.txt', 'w') as fout:
	fout.write(cipher)

print(key)