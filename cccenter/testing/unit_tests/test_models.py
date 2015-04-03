import unittest
from django.db import models
from django.contrib.auth.models import User
from unittest.mock import patch
import models

class TestChallenge(unittest.TestCase):
    @patch(models)
    @patch(models.Challenge)
    def test_ciphertextType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.ciphertext), type(mock_models.TextField))
        
    @patch(models)
    @patch(models.Challenge)
    def test_plaintextType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.plaintext), type(mock_models.TextField))

    @patch(models)
    @patch(models.Challenge)
    def test_ciphertypeType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.ciphertype), type(mock_models.CharField))
        
    @patch(models)
    @patch(models.Challenge)
    def test_cipherkeyType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.cipherkey), type(mock_models.TextField))
        
    @patch(models)
    @patch(models.Challenge)
    def test_forumType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.forum), type(mock_models.ForeignKey))
        
    @patch(models)
    @patch(models.Challenge)
    def test_datetimeCreatedType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.datetime_created), type(mock_models.DateTimeField))
        
    @patch(models)
    @patch(models.Challenge)
    def test_datetimeSolvedType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.datetime_solved), type(mock_models.DateTimeField))
        
    @patch(models)
    @patch(models.Challenge)
    def test_solvedByType(self, mock_challenge, mock_models):
        self.assertEqual(type(mock_challenge.solved_by), type(mock_models.OneToOneField))
        
class TestComment(unittest.TestCase):
    @patch(models)
    @patch(models.Comment)
    def test_usernameType(self, mock_comment, mock_models):
        self.assertEqual(type(mock_comment.username), type(mock_models.TextField))
        
    @patch(models)
    @patch(models.Comment)
    def test_textType(self, mock_comment, mock_models):
        self.assertEqual(type(mock_comment.text), type(mock_models.TextField))
        
    @patch(models)
    @patch(models.Comment)
    def test_datetimeType(self, mock_comment, mock_models):
        self.assertEqual(type(mock_comment.datetime), type(mock_models.DateTimeField))
