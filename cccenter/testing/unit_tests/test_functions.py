import unittest 
import sys

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

class TestCipherFunctions(unittest.TestCase):
	def setUp(self):
		self.text = "Some random TEXT #@#&*(With sOme weIrd,  #$#    characters    "
	def test_ceasar_shift_0(self):
		self.assertTrue(ceasar_shift_encode(self.text, 0) == "SOMERANDOMTEXTWITHSOMEWEIRDCHARACTERS")
	def test_ceasar_shift_2(self):
		self.assertTrue(ceasar_shift_encode(self.text, 2) == "UQOGTCPFQOVGZVYKVJUQOGYGKTFEJCTCEVGTU")
	def test_ceasar_shift_5(self):
		self.assertTrue(ceasar_shift_encode(self.text, 5) == "XTRJWFSITRYJCYBNYMXTRJBJNWIHMFWFHYJWX")

if __name__ == '__main__':
    unittest.main()

