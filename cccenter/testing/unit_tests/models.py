from django.db import models as models_d
from django.contrib.auth.models import User, AnonymousUser
from unittest.mock import patch
from cccenter.models import *
from django.utils import timezone, unittest
from datetime import datetime

class TestChallenge(unittest.TestCase):
    def setUp(self):
        #challenge = models.Challenge()
        #challenge.ciphertext = "abc"
        #challenge.plaintext = "def"
        #challenge.ciphertype = "Caesar Shift Cipher"
        #challenge.cipherkey = "3"
        #challenge.datetime_created = datetime.now()
        #challenge.datetime_solved = datetime.now()
        #challenge.solved_by = User.objects.get(pk=1)
        #challenge.users = [User.objects.get(pk=1)]
        #challenge.forum = [models.Comment.objects.get(pk=1)]
        #challenge.save()
        #self.challenge_id = challenge.id
        #raise Exception(challenge.id)
        #self.members = [attr for attr in dir(models.Challenge) if not callable(attr) and not attr.startswith("__")]
        self.user = User.objects.create(username="m1", password="k")
        self.userprofile = UserProfile(user=self.user, datetime_created=timezone.now())
        self.challenge = Challenge.objects.create(ciphertext="def", plaintext="abc", ciphertype="Caesar Shift Cipher", cipherkey="3",
                                                 datetime_created=timezone.now(), datetime_solved=timezone.now(),
                                                 solved_by=User(), solved=True)
        self.comment = Comment.objects.create(user=self.user, text='hi', datetime=timezone.now(), forum=self.challenge)
        
    def tearDown(self):
        self.user.delete()
        #self.userprofile.delete()
        #self.challenge.delete()
        #self.comment.delete()
        
    def test_ciphertextType(self):
        #challenge = models.Challenge()
        #challenge.ciphertext = "abc"
        #challenge.plaintext = "def"
        #challenge.ciphertype = "Caesar Shift Cipher"
        #challenge.cipherkey = "3"
        #challenge.datetime_created = datetime.now()
        #challenge.datetime_solved = datetime.now()
        #challenge.solved_by = User.objects.get(pk=1)
        #challenge.users = [User.objects.get(pk=1)]
        #challenge.forum = [models.Comment.objects.get(pk=1)]
        #challenge.save()
        #challenge = models.Challenge.objects.get(pk=self.challenge_id)
        #self.assertEqual(challenge.ciphertext, "abc")
        #self.assertEqual(challenge.plaintext, "def")
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        #raise Exception(members)
        self.assertTrue('ciphertext' in members)
        self.assertEqual(self.challenge.ciphertext, "def")
        
    def test_plaintextType(self):
        #self.assertEqual(type(self.challenge.plaintext), models_d.TextField)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('plaintext' in members)

    def test_ciphertypeType(self):
        #self.assertEqual(isinstance(mock_challenge.ciphertype, mock_models.CharField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('ciphertype' in members)
        
    def test_cipherkeyType(self):
        #self.assertEqual(isinstance(mock_challenge.cipherkey, mock_models.TextField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('cipherkey' in members)
        
    def test_datetimeCreatedType(self):
        #self.assertEqual(isinstance(mock_challenge.datetime_created, mock_models.DateTimeField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('datetime_created' in members)
        
    def test_datetimeSolvedType(self):
        #self.assertEqual(isinstance(mock_challenge.datetime_solved, mock_models.DateTimeField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('datetime_solved' in members)
        
    def test_solvedByType(self):
        #self.assertEqual(isinstance(mock_challenge.solved_by, mock_models.OneToOneField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('solved_by' in members)
        
    def test_usersType(self):
        #self.assertEqual(isinstance(mock_challenge.users, mock_models.ManyToManyField), True)
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('users' in members)
        
    def test_challengeTypeType(self):
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('challenge_type' in members)
        
    def test_challengeTypeType(self):
        members = [attr for attr in dir(self.challenge) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('solved' in members)
        
class TestComment(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(username="m1", password="k")
        self.userprofile = UserProfile(user=self.user, datetime_created=timezone.now())
        self.challenge = Challenge.objects.create(ciphertext="def", plaintext="abc", ciphertype="Caesar Shift Cipher", cipherkey="3",
                                                 datetime_created=timezone.now(), datetime_solved=timezone.now(), solved_by=User())
        self.comment = Comment.objects.create(user=self.user, text='hi', datetime=timezone.now(), forum=self.challenge)
        
    def tearDown(self):
        self.user.delete()
        #self.userprofile.delete()
        #self.challenge.delete()
        #self.comment.delete()
        
    def test_userType(self):
        #a = Comment()
        #u = User()
        #a.user = u
        #self.assertEqual(type(a.user), User)
        #self.assertEqual(type(self.comment.user), User)
        members = [attr for attr in dir(self.comment) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('user' in members)
        
    def test_textType(self):
        #a = Comment()
        #a.text = ""
        #self.assertEqual(type(a.text), str)
        members = [attr for attr in dir(Comment(text="")) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('text' in members)
    
    def test_datetimeType(self):
        #a = Comment()
        #a.datetime = timezone.now()
        #self.assertEqual(type(a.datetime), datetime)
        members = [attr for attr in dir(Comment(datetime=None)) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('datetime' in members)
        
    def test_forumType(self):
        #self.assertEqual(isinstance(models.forum, mock_models.ForeignKey), True)
        members = [attr for attr in dir(Comment(forum=Challenge())) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('forum' in members)
        
class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(username="m1", password="k")
        self.userprofile = UserProfile(user=self.user, datetime_created=timezone.now())
        self.challenge = Challenge.objects.create(ciphertext="def", plaintext="abc", ciphertype="Caesar Shift Cipher", cipherkey="3",
                                                 datetime_created=timezone.now(), datetime_solved=timezone.now(), solved_by=User())
        self.comment = Comment.objects.create(user=self.user, text='hi', datetime=timezone.now(), forum=self.challenge)
        
    def tearDown(self):
        self.user.delete()
        self.userprofile.delete()
        #self.userprofile.delete()
        #self.challenge.delete()
        #self.comment.delete()
        
    def test_userType(self):
        #a = UserProfile()
        #u = User()
        #a.user = u
        #self.assertEqual(type(a.user), User)
        #self.assertEqual(type(self.userprofile.user), User)
        members = [attr for attr in dir(self.userprofile) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('user' in members)
        
    def test_datetimeCreatedType(self):
        #a = UserProfile()
        #a.datetime_created = timezone.now()
        #self.assertEqual(type(a.datetime_created), datetime)
        #self.assertEqual(type(self.userprofile.datetime_created), datetime)
        members = [attr for attr in dir(self.userprofile) if not callable(attr) and not attr.startswith("__")]
        self.assertTrue('datetime_created' in members)
