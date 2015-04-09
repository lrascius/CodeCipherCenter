import unittest
import django.db.models as models_d
from django.contrib.auth.models import User
from unittest.mock import patch
import cccenter.models as models
import os
from django.utils import timezone
from datetime import datetime

class TestChallenge(unittest.TestCase):
    def setup(self):
        challenge = models.Challenge()
        challenge.ciphertext = "abc"
        challenge.plaintext = "def"
        challenge.ciphertype = "Caesar Shift Cipher"
        challenge.cipherkey = "3"
        challenge.datetime_created = datetime.now()
        challenge.datetime_solved = datetime.now()
        challenge.solved_by = User.objects.get(pk=1)
        challenge.users = [User.objects.get(pk=1)]
        challenge.forum = [models.Comment.objects.get(pk=1)]
        challenge.save()
        self.challenge_id = challenge.id
        raise Exception(challenge.id)
        
    def test_ciphertextType(self):
        challenge = models.Challenge()
        challenge.ciphertext = "abc"
        challenge.plaintext = "def"
        challenge.ciphertype = "Caesar Shift Cipher"
        challenge.cipherkey = "3"
        challenge.datetime_created = datetime.now()
        challenge.datetime_solved = datetime.now()
        #challenge.solved_by = User.objects.get(pk=1)
        #challenge.users = [User.objects.get(pk=1)]
        #challenge.forum = [models.Comment.objects.get(pk=1)]
        challenge.save()
        #challenge = models.Challenge.objects.get(pk=self.challenge_id)
        self.assertEqual(challenge.ciphertext, "abc")
        self.assertEqual(challenge.plaintext, "def")
        
    def test_plaintextType(self):
        #self.assertEqual(isinstance(mock_challenge.plaintext, mock_models.TextField), True)
        pass

    def test_ciphertypeType(self):
        #self.assertEqual(isinstance(mock_challenge.ciphertype, mock_models.CharField), True)
        pass
        
    def test_cipherkeyType(self):
        #self.assertEqual(isinstance(mock_challenge.cipherkey, mock_models.TextField), True)
        pass
        
    def test_forumType(self):
        #self.assertEqual(isinstance(mock_challenge.forum, mock_models.ForeignKey), True)
        pass
        
    def test_datetimeCreatedType(self):
        #self.assertEqual(isinstance(mock_challenge.datetime_created, mock_models.DateTimeField), True)
        pass
        
    def test_datetimeSolvedType(self):
        #self.assertEqual(isinstance(mock_challenge.datetime_solved, mock_models.DateTimeField), True)
        pass
        
    def test_solvedByType(self):
        #self.assertEqual(isinstance(mock_challenge.solved_by, mock_models.OneToOneField), True)
        pass
        
    def test_challengesType(self):
        #self.assertEqual(isinstance(mock_challenge.users, mock_models.ManyToManyField), True)
        pass
        
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
