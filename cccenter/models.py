#!cccenter/models.py
'''This file contains the Django models for the cccenter app.'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

# Create your models here.

class UserProfile(models.Model):
    '''
    A model for user profile objects.

    :field user: (models.User) The associated User object
    :field profile_image: (models.ImageField) The image associated with the user
    '''
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to='images/profile',
                                      default='images/profile/default.png')

    def __unicode__(self):
        return smart_text(self.user)

class Cipher(models.Model):
    '''
    A model for cipher objects

    :field ciphertype: (models.CharField) The cipher's name
    :field difficulty: (models.CharField) The cipher's difficulty
    '''
    ciphertype = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=50, choices=(('beginner', 'Beginner'),
                                                          ('intermediate', 'Intermediate'),
                                                          ('advanced', 'Advanced')))

    def __unicode__(self):
        return smart_text(self.ciphertype)

class Challenge(models.Model):
    '''
    A model for challenge objects.

    :field ciphertext: (models.TextField) The challenge's ciphertext
    :field plaintext: (models.TextField) The challenge's plaintext
    :field ciphertype: (models.CharField) The name of the cipher used
    :field cipherkey: (models.TextField) The challenge's cipher key
    :field users: (models.ManyToManyField) The users registered in the challenge\
    (related_name="user_challenge_set")
    :field datetime_created: (models.DateTimeField) The date and time the challenge was created
    :field datetime_solved: (models.DateTimeField) The date and time the challenge was solved
    :field solved_by: (models.ManyToManyField) The users who have solved the challenge
    :field challenge_type: (models.CharField) The type of challenge (single, collaborative,\
    competitive)
    :field solved: (models.BooleanField) If the challenge has been solved
    :field cipher: (models.ManyToManyField) The cipher objects the challenge is related to
    '''
    ciphertext = models.TextField(default="")
    plaintext = models.TextField(default="")
    ciphertype = models.CharField(max_length=200)
    cipherkey = models.TextField(default="")
    users = models.ManyToManyField(User, related_name="user_challenge_set", blank=True, null=True)
    datetime_created = models.DateTimeField()
    datetime_solved = models.DateTimeField(blank=True, null=True)
    solved_by = models.ManyToManyField(User, related_name="user_solved_challenge_set",
                                       blank=True, null=True)
    challenge_type = models.CharField(max_length=50, choices=(('single', 'Single'),
                                                              ('collaborative', 'Collaborative'),
                                                              ('competitive', 'Competitive')))
    solved = models.BooleanField(default=False)
    cipher = models.ManyToManyField(Cipher, related_name="cipher_challenge_set")

    def __unicode__(self):
        return smart_text(self.ciphertype)


class Comment(models.Model):
    '''
    A model for comments in the forums.

    :field user: (models.ForeignKey) The user who posted the comment
    :field text: (models.TextField) The text in the comment
    :field datetime: (models.DateTimeField) The date and time the comment was posted
    :field forum: (models.ForeignKey) The forum the comment belongs to (linked to a challenge)
    '''
    user = models.ForeignKey(User, related_name='user_comment_set')
    text = models.TextField(default="")
    datetime = models.DateTimeField()
    forum = models.ForeignKey(Challenge, related_name='challenge_comment_set')

    def __unicode__(self):
        return smart_text(self.user)

class Notification(models.Model):
    '''
    A model for push notifications.

    :field user: (models.ForeignKey) The user who the notification is sent to
    :field notification: (models.CharField) The text in the notification
    :field link: (models.CharField) The link to what the notification is about
    :field viewed: (models.BooleanField) Whether or not the notification has been viewed
    :field datetime: (models.DateTimeField) When the notification was created
    '''
    user = models.ForeignKey(User)
    notification = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    viewed = models.BooleanField(default=False)
    datetime = models.DateTimeField()

    def __unicode__(self):
        return smart_text(self.user)

