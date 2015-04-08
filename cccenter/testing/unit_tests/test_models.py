import django
django.setup()
import unittest
import django.db.models as models_d
from django.contrib.auth.models import User
from unittest.mock import patch
import cccenter.models as models
import os
from django.utils import timezone
from datetime import datetime

class TestChallenge(unittest.TestCase):
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_ciphertextType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.ciphertex, mock_models.TextField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_plaintextType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.plaintext, mock_models.TextField), True)

    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_ciphertypeType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.ciphertype, mock_models.CharField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_cipherkeyType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.cipherkey, mock_models.TextField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_forumType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.forum, mock_models.ForeignKey), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_datetimeCreatedType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.datetime_created, mock_models.DateTimeField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_datetimeSolvedType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.datetime_solved, mock_models.DateTimeField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_solvedByType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.solved_by, mock_models.OneToOneField), True)
        
    @patch('django.db.models')
    @patch('cccenter.models.Challenge')
    def test_challengesType(self, mock_challenge, mock_models):
        self.assertEqual(isinstance(mock_challenge.users, mock_models.ManyToManyField), True)
        
class TestComment(unittest.TestCase):
    def test_userType(self):
        a = models.Comment()
        u = User()
        a.user = u
        self.assertEqual(type(a.user), User)
        
    def test_textType(self):
        a = models.Comment()
        a.text = ""
        self.assertEqual(type(a.text), str)
    
    def test_datetimeType(self):
        a = models.Comment()
        a.datetime = timezone.now()
        self.assertEqual(type(a.datetime), datetime)
        
class TestUserProfile(unittest.TestCase):
    def test_userType(self):
        a = models.UserProfile()
        u = User()
        a.user = u
        self.assertEqual(type(a.user), User)
        
    def test_datetimeCreatedType(self):
        a = models.UserProfile()
        a.datetime_created = timezone.now()
        self.assertEqual(type(a.datetime_created), datetime)
