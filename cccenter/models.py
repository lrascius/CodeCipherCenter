#!cccenter/models.py
'''This file contains Django the models for the cccenter app.'''
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Challenge(models.Model):
    '''A model for ciphertext display and plaintext submission.  Contains
       fields for the ciphertext (display only) and the plantext.'''
    ciphertext = models.TextField()
    plaintext = models.TextField()

class UserProfile(models.Model):
    '''A model for storing users.'''
    user = models.OneToOneField(User)
    challenges = models.ManyToManyField(Challenge)
