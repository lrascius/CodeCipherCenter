'''Generates challenge lists'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone

def challenge_list():
    chList = []
    i = models.Challenge.objects.all()

    for names in i:
        chList.append(names.id)

def join_challenge(challenge_id, user_id):
    if type(challenge_id) is not int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")
        
    if type(user_id) is not int:
        raise TypeError("user_id is " + str(type(challenge_id)) + ", not int")
        
    challenge = models.Challenge.objects.get(pk=challenge_id)
    
    if challenge is None:
        raise ValueError("challenge_id is invalid")
        
    user = User.objects.get(pk=user_id)
    
    if user is None:
        raise ValueError("user_id is invalid")
        
    challenge.users.add(user)
    challenge.save()
