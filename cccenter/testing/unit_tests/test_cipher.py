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
        self.client.login(username='marctest0', password='test0')
        
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.client.logout()
        
    def test_ceasar_shift_0(self):
        self.assertTrue(ceasar_shift_encode(self.text, 0) == "SOMERANDOMTEXTWITHSOMEWEIRDCHARACTERS")
        
    def test_ceasar_shift_2(self):
        self.assertTrue(ceasar_shift_encode(self.text, 2) == "UQOGTCPFQOVGZVYKVJUQOGYGKTFEJCTCEVGTU")
        
    def test_ceasar_shift_5(self):
        self.assertTrue(ceasar_shift_encode(self.text, 5) == "XTRJWFSITRYJCYBNYMXTRJBJNWIHMFWFHYJWX")
        
    @mock.patch('cccenter.Cipher')
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_createchallenge(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
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
        mock_cipher.objects.get.assert_called_with(ciphertype=self.challengetype)
        mock_challenge.cipher.add.assert_called_with(mock_cipher)
        
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
        
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionPass1(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value = "user"
        mock_challenge.plaintext = 'abc'
        
        success = check_solution(challenge_id=1, user_id=2, guessed_plaintext='abc')
        
        mock_models.Challenge.objects.get.assert_called_with(pk=1)
        mock_user.objects.get.assert_called_with(pk=2)
        self.assertTrue(success)
        self.assertEqual(mock_challenge.solved_by, "user")
        self.assertEqual(mock_challenge.datetime_solved, "now")
        self.assertTrue(mock_challenge.solved)
        self.assertTrue(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionPass2(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        mock_challenge.plaintext = 'abc'
        mock_challenge.solved = True
        
        success = check_solution(challenge_id=1, user_id=2, guessed_plaintext='abc')
        
        mock_models.Challenge.objects.get.assert_called_with(pk=1)
        mock_user.objects.get.assert_called_with(pk=2)
        self.assertTrue(success)
        self.assertNotEqual(mock_challenge.solved_by, "user")
        self.assertNotEqual(mock_challenge.datetime_solved, "now")
        self.assertTrue(mock_challenge.solved)
        self.assertFalse(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionFail1(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        mock_challenge.plaintext = 'abc'
        
        success = check_solution(challenge_id=1, user_id=2, guessed_plaintext='def')
        
        mock_models.Challenge.objects.get.assert_called_with(pk=1)
        mock_user.objects.get.assert_called_with(pk=2)
        self.assertFalse(success)
        
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionFail2(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        mock_challenge.plaintext = 'abc'
        
        with self.assertRaises(TypeError):
            success = check_solution(challenge_id='1', user_id=2, guessed_plaintext='abc')
            
        with self.assertRaises(TypeError):
            success = check_solution(challenge_id=1.0, user_id=2, guessed_plaintext='abc')
            
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionFail3(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        mock_challenge.plaintext = 'abc'
        
        with self.assertRaises(TypeError):
            success = check_solution(challenge_id=1, user_id='2', guessed_plaintext='abc')
            
        with self.assertRaises(TypeError):
            success = check_solution(challenge_id=1, user_id=2.0, guessed_plaintext='abc')
            
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionFail4(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= None
        mock_challenge.plaintext = 'abc'
        
        with self.assertRaises(ValueError):
            success = check_solution(challenge_id=-1, user_id=2, guessed_plaintext='abc')
            
    @mock.patch('cccenter.python.cipher.timezone')
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_checksolutionFail5(self, mock_challenge, mock_models, mock_user, mock_timezone):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.get.return_value = None
        mock_user.objects.get.return_value= "user"
        mock_challenge.plaintext = 'abc'
        
        with self.assertRaises(ValueError):
            success = check_solution(challenge_id=1, user_id=-2, guessed_plaintext='abc')

    def test_create_ciphertext(self):
        ciphertext = create_ciphertext("Caesar Shift", self.text)      
        self.assertTrue(ceasar_shift_encode(self.text, ciphertext['cipherkey']) == ciphertext['ciphertext'])

        ciphertext = create_ciphertext("Multiplicitive", self.text)      
        self.assertTrue(multiplicitive_cipher(self.text, ciphertext['cipherkey']) == ciphertext['ciphertext'])

class TestMultiplicitiveCipher(TestCase):
    def setUp(self):
        self.text = "#32344  ABCDEfgHIJKLMNOpqrSTUVWXYZ ? 3232 /32"
        
    def test_multiplicitive_cipher_mult1(self):
        self.assertTrue(multiplicitive_cipher(self.text, 1) == "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                                                                
    def test_multiplicitive_cipher_mult3(self):
        self.assertTrue(multiplicitive_cipher(self.text, 3) == "CFILORUXADGJMPSVYBEHKNQTWZ")

    def test_multiplicitive_cipher_mult5(self):
        self.assertTrue(multiplicitive_cipher(self.text, 5) == "EJOTYDINSXCHMRWBGLQVAFKPUZ")

    def test_multiplicitive_even_mult2(self):
        with self.assertRaises(Exception) as context:
            multiplicitive_cipher(self.text, 2)
        self.assertEqual("Even key is invalid for a multiplicitive cipher", str(context.exception))

    def test_multiplicitive_even_mult10(self):
        with self.assertRaises(Exception) as context:
            multiplicitive_cipher(self.text, 10)
        self.assertEqual("Even key is invalid for a multiplicitive cipher", str(context.exception))

class TestAffineCipher(TestCase):
    def setUp(self):
        self.text = "# $# d $r (i n k w a t e r ? 3232 /32"
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    def test_affine_cipher(self):
        self.assertTrue(affine_cipher(self.text, 239, 152) == "PHONYGARUH")

    def test_affine_cipher2(self):
        self.assertTrue(affine_cipher(self.alphabet, 15, 12) == "APETIXMBQFUJYNCRGVKZODSHWL")

    def test_affine_cipher_even2(self):
        with self.assertRaises(Exception) as context:
            affine_cipher(self.text, 2, 15)
        self.assertEqual("Invalid value for a in affine cipher", str(context.exception))
 
    def test_affine_cipher_mod13(self):
        with self.assertRaises(Exception) as context:
            affine_cipher(self.text, 13, 12)
        self.assertEqual("Invalid value for a in affine cipher", str(context.exception))

