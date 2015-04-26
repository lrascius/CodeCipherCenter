from django.test import TestCase
from cccenter.python.challenge import *
import cccenter.models as models
import mock

class TestChallenge(TestCase):

	@mock.patch('cccenter.python.challenge.User')
	@mock.patch('cccenter.python.challenge.models')
	@mock.patch('cccenter.python.challenge.models.Challenge')
	def test_challengeList(self, mock_challenge, mock_models, mock_user):
		
    	#    a = challenge_list()
    	#    self.assertEqual(type(a), str)
    	#    self.assertGreater(len(a), 0)
        
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
        mock_user.user_challenge_set.filter.assert_called_with(pk=1)
        #mock_models.Challenge.user_set.filter.assert_called_with(pk=2)
        
    @mock.patch('cccenter.python.challenge.User')
    @mock.patch('cccenter.python.challenge.models')
    @mock.patch('cccenter.python.challenge.models.Challenge')
    def test_userInChallenge_Pass2(self, mock_challenge, mock_models, mock_user):
        mock_user.user_challenge_set.filter.return_value = mock_user
        #mock_models.Challenge.objects.get.return_value = mock_challenge
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.exists.return_value = False
        mock_user.id = 2
        
        success = user_in_challenge(challenge_id=1, user=mock_user)
        
        self.assertFalse(success)
        mock_user.user_challenge_set.filter.assert_called_with(pk=1)
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
        #mock_models.Challenge.objects.get.return_value = mock_challenge
        #mock_challenge.user_set.filter.return_value = mock_user
        mock_user.exists.return_value = True
        mock_user.id = 2
        
        with self.assertRaises(ValueError):
            success = user_in_challenge(challenge_id=-1, user=mock_user)
