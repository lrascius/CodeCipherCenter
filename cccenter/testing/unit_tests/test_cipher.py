from django.test import TestCase
from cccenter.python.cipher import *
from django.utils import timezone
from cccenter.models import *
import mock

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
        
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_createchallenge(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        #mock_models.Challenge.users.add.return_value = ""
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn, True, self.tn, self.user1)
                                            
        self.assertFalse(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created=self.tn)
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        #self.assertEqual(a.datetime_created, self.tn)
        #self.assertEqual(a.datetime_solved, self.tn)
        #self.assertEqual(a.solved_by, self.user1)
        
        #a.delete()
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn, self.tn)
                                            
        self.assertFalse(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created=self.tn)
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        #self.assertEqual(a.datetime_created, self.tn)
        #self.assertEqual(a.datetime_solved, self.tn)
        #self.assertEqual(a.solved_by, None)
        
        #a.delete()
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn)
                                            
        self.assertFalse(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created=self.tn)
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        #self.assertEqual(a.datetime_created, self.tn)
        #self.assertEqual(a.datetime_solved, None)
        
        #a.delete()
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users)
                                            
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, self.users)
        #self.assertEqual(a.datetime_created, self.tn)
        
        #a.delete()
        
        mock_challenge.users.add.called = False # set to false after previous tests
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype)
        
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertFalse(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, None)
        
        #a.delete()
        
        mock_challenge.users.add.called = False # set to false after previous tests
        
        with self.assertRaises(ValueError):
            c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype, solved=True)
        
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertFalse(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, None)
        
        #a.delete()
        
        mock_challenge.users.add.called = False # set to false after previous tests
        
        with self.assertRaises(ValueError):
            c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                  solved=True, dt_solved=self.tn)
        
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertFalse(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
        #a = Challenge.objects.get(pk=c_data['challenge_id'])
        #self.assertEqual(a.ciphertext, self.ciphertext)
        #self.assertEqual(a.plaintext, self.plaintext)
        #self.assertEqual(a.ciphertype, self.ciphertype)
        #self.assertEqual(a.cipherkey, self.key)
        #self.assertEqual(a.challenge_type, self.challengetype)
        #self.assertEqual(a.users, None)
        
        #a.delete()

if __name__ == '__main__':
    unittest.main()

