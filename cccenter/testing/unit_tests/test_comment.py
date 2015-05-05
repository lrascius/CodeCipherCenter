from django.test import TestCase
from cccenter.python.comment import *
import mock

class TestComment(TestCase):
    @mock.patch('cccenter.python.comment.Comment')
    @mock.patch('cccenter.python.comment.Challenge')
    @mock.patch('cccenter.python.comment.User')
    @mock.patch('cccenter.python.comment.models')
    def test_get_comments_Pass1(self, mock_comment, mock_challenge, mock_user, mock_models):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_challenge.challenge_comment_set.all.return_value = [mock_comment]
        
        comments = get_comments(challenge_id=1)
        
        self.assertEqual(comments, [mock_comment])
        
    @mock.patch('cccenter.python.comment.Comment')
    @mock.patch('cccenter.python.comment.Challenge')
    @mock.patch('cccenter.python.comment.User')
    @mock.patch('cccenter.python.comment.models')
    def test_get_comments_Fail1(self, mock_comment, mock_challenge, mock_user, mock_models):
        mock_models.Challenge.objects.get.return_value = mock_challenge
        mock_challenge.challenge_comment_set.return_value = [mock_comment]
        
        with self.assertRaises(TypeError):
            comments = get_comments(challenge_id=1.0)
        with self.assertRaises(TypeError):
            comments = get_comments(challenge_id='1')
            
    @mock.patch('cccenter.python.comment.Comment')
    @mock.patch('cccenter.python.comment.Challenge')
    @mock.patch('cccenter.python.comment.User')
    @mock.patch('cccenter.python.comment.models')
    def test_get_comments_Fail2(self, mock_comment, mock_challenge, mock_user, mock_models):
        mock_models.Challenge.objects.get.return_value = None
        mock_challenge.challenge_comment_set.return_value = [mock_comment]
        
        with self.assertRaises(ValueError):
            comments = get_comments(challenge_id=-1)
