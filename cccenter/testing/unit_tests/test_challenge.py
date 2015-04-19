from django.test import TestCase
from cccenter.python.challenge import *
import cccenter.models as models
import mock

class TestChallenge(TestCase):
    def test_challengeList(self):
        a = challenge_list()
        self.assertEqual(type(a), str)
        self.assertGreater(len(a), 0)
        
    @mock.patch('cccenter.python.cipher.User')
    @mock.patch('cccenter.python.cipher.models')
    @mock.patch('cccenter.python.cipher.models.Challenge')
    def test_joinChallenge_Pass1(self, mock_challenge, mock_models, mock_user):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_user.objects.get.return_value= "user"
        
        success = join_challenge(challenge_id=1, user_id=2)
        
        mock_challenges.users.add.assert_called_with("user")
