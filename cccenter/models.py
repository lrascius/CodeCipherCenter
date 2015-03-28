#!cccenter/models.py
'''This file contains Django the models for the cccenter app.'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode

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

class SignUp(models.Model):
	username = models.CharField(max_length=64)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64, null=True, blank=True)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return smart_unicode(self.email)
