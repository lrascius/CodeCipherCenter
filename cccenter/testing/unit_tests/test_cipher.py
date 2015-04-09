import unittest 
import sys
from cccenter.python.cipher import *

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

