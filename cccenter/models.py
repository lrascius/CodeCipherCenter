#!cccenter/models.py
'''This file contains Django the models for the cccenter app.'''
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    '''A model for comments in the forums.'''
    username = models.CharField(max_length=50)
    text = models.TextField(default="")
    datetime = models.DateTime()

class UserProfile(models.Model):
    '''A model for storing users.'''
    user = models.OneToOneField(User)

class Challenge(models.Model):
    '''A model for ciphertext display and plaintext submission.  Contains
       fields for the ciphertext (display only) and the plantext.'''
    ciphertext = models.TextField(default="")
    plaintext = models.TextField(default="")
    ciphertype = models.CharField(max_length=200)
    cipherkey = models.TextField(default="")
    forum = models.ForeignKey(Comment)
    users = models.ManyToManyField(UserProfile)
