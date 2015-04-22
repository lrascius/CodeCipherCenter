#!cccenter/models.py
'''This file contains Django the models for the cccenter app.'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

# Create your models here.

class UserProfile(models.Model):
    '''A model for storing users.'''
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to='images/profile',
                                      default='images/profile/default.png')

    def __unicode__(self):
        return smart_text(self.user)

class Challenge(models.Model):
    '''A model for ciphertext display and plaintext submission.  Contains
       fields for the ciphertext (display only) and the plantext.'''
    ciphertext = models.TextField(default="")
    plaintext = models.TextField(default="")
    ciphertype = models.CharField(max_length=200)
    cipherkey = models.TextField(default="")
    users = models.ManyToManyField(User, related_name="joined", blank=True, null=True)
    datetime_created = models.DateTimeField()
    datetime_solved = models.DateTimeField(blank=True, null=True)
    solved_by = models.OneToOneField(User, blank=True, null=True)
    challenge_type = models.CharField(max_length=50, choices=(('single', 'single'),
                                                              ('collaborative', 'collaborative'),
                                                              ('competitive', 'competitive')))
    solved = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_text(self.ciphertype)


class Comment(models.Model):
    '''A model for comments in the forums.'''
    user = models.OneToOneField(User)
    text = models.TextField(default="")
    datetime = models.DateTimeField()
    forum = models.ForeignKey(Challenge)

    def __unicode__(self):
        return smart_text(self.user)
