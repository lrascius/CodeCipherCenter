from django.test import TestCase
from cccenter.python.challenge import *
import mock

class TestChallenge(TestCase):
    def setUp(self):
        self.text = "Some random TEXT #@#&*(With sOme weIrd,  #$#    characters    "
        self.tn = 'now'
        self.plaintext = "abc"
        self.ciphertext = "DEF"
        self.ciphertype = "Caesar Shift Cipher"
        self.key = "3"
        self.user1 = 'user1'
        self.user2 = 'user2'
        self.users = [self.user1, self.user2]
        self.challengetype = 'single'
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass1(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
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
        mock_cipher.objects.get.assert_called_with(ciphertype=self.ciphertype)
        mock_challenge.cipher.add.assert_called_with(mock_cipher)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass2(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn)
                                            
        self.assertFalse(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created=self.tn)
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass3(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):    
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users)
                                            
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass4(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        mock_challenge.users.add.called = False # set to false after previous tests
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype)
        
        self.assertTrue(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created="now")
        self.assertFalse(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass5(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        mock_challenge.users.add.called = False # set to false after previous tests
        
        with self.assertRaises(ValueError):
            c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype, solved=True)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass6(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        mock_challenge.users.add.called = False # set to false after previous tests
        
        with self.assertRaises(ValueError):
            c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                  solved=True, dt_solved=self.tn)
        
    @mock.patch('cccenter.python.challenge.Cipher')
    @mock.patch('cccenter.python.challenge.timezone')
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_createchallenge_Pass7(self, mock_challenge, mock_models, mock_user, mock_timezone, mock_cipher):
        mock_timezone.now.return_value = "now"
        mock_models.Challenge.objects.create.return_value = mock_challenge
        mock_cipher.objects.get.return_value = mock_cipher
        
        c_data = create_challenge(self.plaintext, self.ciphertext, self.ciphertype, self.key, self.challengetype,
                                            self.users, self.tn, self.tn)
                                            
        self.assertFalse(mock_timezone.now.called)
        self.assertTrue(mock_models.Challenge.objects.create.called)
        mock_models.Challenge.objects.create.assert_called_with(plaintext=self.plaintext, ciphertext=self.ciphertext,
                                                                ciphertype=self.ciphertype, cipherkey=self.key,
                                                                challenge_type=self.challengetype, datetime_created=self.tn)
        self.assertTrue(mock_challenge.users.add.called)
        self.assertTrue(mock_challenge.save.called)

    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_challengeList(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.all.return_value = [mock_challenge]
        
        res = challenge_list()
        
        self.assertEqual(res, [mock_challenge])
        self.assertTrue(mock_models.Challenge.objects.all.called)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Pass1(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        mock_challenge.users.add.return_value = True
        
        join_challenge(challenge_id=1, user_id=2)
        
        mock_challenge.users.add.assert_called_with("user")
        self.assertTrue(mock_challenge.save.called)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Pass2(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_challenge.challenge_type = 'single'
        
        res = join_challenge(challenge_id=1, user_id=2)
        
        self.assertFalse(res)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Fail1(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = None
        mock_user.objects.get.return_value= "user"
        
        with self.assertRaises(ValueError):
            join_challenge(challenge_id=-1, user_id=2)
            
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Fail2(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = None
        mock_user.objects.get.return_value= "user"
        
        with self.assertRaises(ValueError):
            join_challenge(challenge_id=1, user_id=-2)
            
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Fail3(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = None
        mock_user.objects.get.return_value= "user"
        
        with self.assertRaises(TypeError):
            join_challenge(challenge_id=1.0, user_id=2)
            
        with self.assertRaises(TypeError):
            join_challenge(challenge_id='1', user_id=2)
            
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_joinChallenge_Fail4(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = None
        mock_user.objects.get.return_value= "user"
        
        with self.assertRaises(TypeError):
            join_challenge(challenge_id=1, user_id=2.0)
            
        with self.assertRaises(TypeError):
            join_challenge(challenge_id=1, user_id='2')
            
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_getCiphertext_Pass1(self, mock_challenge, mock_models):
        mock_models.Challenge.objects.get.return_value = mock_models
        mock_models.ciphertext = "DEF"
        
        ct = get_ciphertext(challenge_id=1)
        
        self.assertEqual(mock_models.ciphertext, ct)
        
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_getCiphertext_Fail1(self, mock_challenge, mock_models):
        mock_models.Challenge.objects.get.return_value = None
        mock_models.ciphertext = "DEF"
        
        with self.assertRaises(ValueError):
            ct = get_ciphertext(challenge_id=-1)
            
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_getCiphertext_Fail2(self, mock_challenge, mock_models):
        mock_models.Challenge.objects.get.return_value = None
        mock_models.ciphertext = "DEF"
        
        with self.assertRaises(TypeError):
            ct = get_ciphertext(challenge_id='1')
            
        with self.assertRaises(TypeError):
            ct = get_ciphertext(challenge_id=1.0)
            
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_userInChallenge_Pass1(self, mock_challenge, mock_models, mock_user):
        mock_user.user_challenge_set.filter.return_value = mock_user
        #mock_models.Challenge.objects.get.return_value = mock_challenge
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.exists.return_value = True
        mock_user.id = 2
        
        success = user_in_challenge(challenge_id=1, user=mock_user)
        
        self.assertTrue(success)
        mock_user.user_challenge_set.get.assert_called_with(pk=1)
        #mock_models.Challenge.user_set.filter.assert_called_with(pk=2)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_userInChallenge_Pass2(self, mock_challenge, mock_models, mock_user):
        mock_user.user_challenge_set.filter.return_value = mock_user
        #mock_models.Challenge.objects.get.return_value = mock_challenge
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.user_challenge_set.get.return_value = None
        mock_user.id = 2
        
        success = user_in_challenge(challenge_id=1, user=mock_user)
        
        self.assertEqual(success, (False, False))
        mock_user.user_challenge_set.get.assert_called_with(pk=1)
        #mock_models.Challenge.user_set.filter.assert_called_with(pk=2)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_userInChallenge_Fail1(self, mock_challenge, mock_models, mock_user):
        mock_user.user_challenge_set.filter.return_value = mock_user
        #mock_models.Challenge.objects.get.return_value = mock_challenge
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.exists.return_value = True
        mock_user.id = 2
        
        with self.assertRaises(TypeError):
            success = user_in_challenge(challenge_id='1', user=mock_user)
        
        with self.assertRaises(TypeError):
            success = user_in_challenge(challenge_id=1.0, user=mock_user)
            
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_userInChallenge_Fail2(self, mock_challenge, mock_models, mock_user):
        mock_user.user_challenge_set.filter.return_value = mock_user
        mock_models.Challenge.objects.get.return_value = None
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.exists.return_value = True
        mock_user.id = 2
        
        with self.assertRaises(ValueError):
            success = user_in_challenge(challenge_id=-1, user=mock_user)

    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    @mock.patch('cccenter.python.challenge.models.Cipher')
    def test_get_difficulty_Pass1(self, mock_cipher, mock_challenge, mock_models):
        mock_challenge.cipher.all.return_value = [mock_cipher]
        mock_cipher.difficulty = 'beginner'
        mock_models.Challenge.objects.get.return_value = mock_challenge
        
        difficulty = get_difficulty(challenge_id=1)
        
        self.assertEqual(difficulty, mock_cipher.difficulty)
    
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    @mock.patch('cccenter.python.challenge.models.Cipher')
    @mock.patch('cccenter.python.challenge.models.Cipher')   
    @mock.patch('cccenter.python.challenge.models.Cipher')
    def test_get_difficulty_Pass2(self, mock_cipher1, mock_cipher2, mock_cipher3, mock_challenge, mock_models):
        mock_challenge.cipher.all.return_value = [mock_cipher1, mock_cipher2, mock_cipher3]
        mock_cipher1.difficulty = 'beginner'
        mock_cipher2.difficulty = 'intermediate'
        mock_cipher3.difficulty = 'advanced'
        mock_models.Challenge.objects.get.return_value = mock_challenge
        
        difficulty = get_difficulty(challenge_id=1)
        
        self.assertEqual(difficulty, 'advanced')
        
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    @mock.patch('cccenter.python.challenge.models.Cipher')
    def test_get_difficulty_Fail1(self,  mock_cipher, mock_challenge, mock_models):
        mock_challenge.cipher.all.return_value = [mock_cipher]
        mock_cipher.difficulty = 'beginner'
        mock_models.Challenge.objects.get.return_value = mock_challenge
        
        with self.assertRaises(TypeError):
            difficulty = get_difficulty(challenge_id=1.0)
        with self.assertRaises(TypeError):
            difficulty = get_difficulty(challenge_id='1')
            
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_get_challenge_info_Pass1(self, mock_challenge, mock_models):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_challenge.users.all.return_value = ['u1', 'u2']
        mock_challenge.datetime_created = "now1"
        mock_challenge.datetime_solved = "now2"
        mock_challenge.solved_by.all.return_value = ['user1', 'user2']
        mock_challenge.challenge_type = 'beginner'
        mock_challenge.solved = True
        
        res = get_challenge_info(challenge_id=1)
        
        mock_models.Challenge.objects.get.assert_called_with(pk=1)
        self.assertEqual(res['datetime_created'], mock_challenge.datetime_created)
        self.assertEqual(res['datetime_solved'], mock_challenge.datetime_solved)
        self.assertEqual(res['solved_by'], ['user1', 'user2'])
        self.assertEqual(res['challenge_type'], mock_challenge.challenge_type)
        self.assertEqual(res['solved'], mock_challenge.solved)
        self.assertEqual(res['users'], ['u1', 'u2'])
        
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_get_challenge_info_Fail1(self, mock_challenge, mock_models):
        with self.assertRaises(TypeError):
            res = get_challenge_info(challenge_id=1.0)
        with self.assertRaises(TypeError):
            res = get_challenge_info(challenge_id='1')
