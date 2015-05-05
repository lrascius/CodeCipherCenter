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
        mock_challenge.challenge_comment_set.return_value = [mock_comment]
        
        comments = get_comments(challenge_id=1)
        
        self.assertEqual(comments, [mock_comment])
        
    
