from django.test import TestCase
from cccenter.python.cipher import *
from django.utils import timezone
from cccenter.models import *

class TestCipherFunctions(TestCase):
    def setUp(self):
        self.text = "Some random TEXT #@#&*(With sOme weIrd,  #$#    characters    "
        self.tn = timezone.now()
        self.plaintext = "abc"
        self.ciphertext = "DEF"
        self.ciphertype = "Caesar Shift Cipher"
        self.key = "3"
        self.user1 = User.objects.create(username="t1")
        self.user1.save()
        self.user2 = User.objects.create(username="t2")
        self.user2.save()
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
        ciphertext, c_id = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn, self.tn, self.user1)
        a = Challenge.objects.get(pk=c_id)
        self.assertEqual(a.ciphertext, self.ciphertext)
        self.assertEqual(a.plaintext, self.plaintext)
        self.assertEqual(a.ciphertype, self.ciphertype)
        self.assertEqual(a.cipherkey, self.key)
        self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        self.assertEqual(a.datetime_created, self.tn)
        self.assertEqual(a.datetime_solved, self.tn)
        self.assertEqual(a.solved_by, self.user1)
        
        a.delete()
        
        ciphertext, c_id = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn, self.tn)
        a = Challenge.objects.get(pk=c_id)
        self.assertEqual(a.ciphertext, self.ciphertext)
        self.assertEqual(a.plaintext, self.plaintext)
        self.assertEqual(a.ciphertype, self.ciphertype)
        self.assertEqual(a.cipherkey, self.key)
        self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        self.assertEqual(a.datetime_created, self.tn)
        self.assertEqual(a.datetime_solved, self.tn)
        self.assertEqual(a.solved_by, None)
        
        a.delete()
        
        ciphertext, c_id = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn)
        a = Challenge.objects.get(pk=c_id)
        self.assertEqual(a.ciphertext, self.ciphertext)
        self.assertEqual(a.plaintext, self.plaintext)
        self.assertEqual(a.ciphertype, self.ciphertype)
        self.assertEqual(a.cipherkey, self.key)
        self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        self.assertEqual(a.datetime_created, self.tn)
        self.assertEqual(a.datetime_solved, None)
        
        a.delete()
        
        ciphertext, c_id = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users)
        a = Challenge.objects.get(pk=c_id)
        self.assertEqual(a.ciphertext, self.ciphertext)
        self.assertEqual(a.plaintext, self.plaintext)
        self.assertEqual(a.ciphertype, self.ciphertype)
        self.assertEqual(a.cipherkey, self.key)
        self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        self.assertEqual(a.datetime_created, self.tn)
        
        a.delete()
        
        ciphertext, c_id = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype)
        a = Challenge.objects.get(pk=c_id)
        self.assertEqual(a.ciphertext, self.ciphertext)
        self.assertEqual(a.plaintext, self.plaintext)
        self.assertEqual(a.ciphertype, self.ciphertype)
        self.assertEqual(a.cipherkey, self.key)
        self.assertEqual(a.challenge_type, self.challengetype)
        self.assertEqual(a.users, None)
        
        a.delete()

if __name__ == '__main__':
    unittest.main()

