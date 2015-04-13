from django.test import TestCase
from cccenter.python.cipher import *
from django.utils import timezone

class TestCipherFunctions(TestCase):
	def setUp(self):
		self.text = "Some random TEXT #@#&*(With sOme weIrd,  #$#    characters    "
		self.tn = timezone.now()
		self.plaintext = "abc"
		self.ciphertext = "DEF"
		self.ciphertype = "Caesar Shift Cipher"
		self.key = "3"
		self.user1 = User.objects.create(username="t1")
		self.user2 = User.objects.create(username="t2")
		self.users = [self.user1, self.user2]
		self.challengetype = 'single'
		
	def tearDown(self):
	    self.user1.delete()
	    self.user2.delete()
		
	def test_ceasar_shift_0(self):
		self.assertTrue(ceasar_shift_encode(self.text, 0) == "SOMERANDOMTEXTWITHSOMEWEIRDCHARACTERS")
		
	def test_ceasar_shift_2(self):
		self.assertTrue(ceasar_shift_encode(self.text, 2) == "UQOGTCPFQOVGZVYKVJUQOGYGKTFEJCTCEVGTU")
		
	def test_ceasar_shift_5(self):
		self.assertTrue(ceasar_shift_encode(self.text, 5) == "XTRJWFSITRYJCYBNYMXTRJBJNWIHMFWFHYJWX")
		
	def test_createchallenge(self):
	    ciphertext, c_id = createChallenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.users,
	                                       self.tn, self.tn, self.user1, self.challengetype)
	    

if __name__ == '__main__':
    unittest.main()

