# Function that applies a ceasar shift on a piece of text. The encrypted text is returned. 
def ceasar_shift_encode(text, shift):
	# List of 26 lowercase letters
	alphabet = list(map(chr, range(97, 123)))

	encoded_text = ""
	text = "".join(text.lower().split())
	for char in text:
		if(char in alphabet):
			char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
			encoded_text += char
	return encoded_text.upper()


