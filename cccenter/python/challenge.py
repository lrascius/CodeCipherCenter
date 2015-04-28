'''Generates challenge lists'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone

def challenge_list():
    '''Returns a list of the challenges in the database.'''
    chList = []
    i = models.Challenge.objects.all()

    for names in i:
        chList.append(names.id)

def join_challenge(challenge_id, user_id):
    '''Adds the given user to the given challenge.'''
    if type(challenge_id) is not int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    if type(user_id) is not int:
        raise TypeError("user_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("challenge_id is invalid")

    user = User.objects.get(pk=user_id)

    if user == None:
        raise ValueError("user_id is invalid")

    challenge.users.add(user)
    challenge.save()
    return True

def get_ciphertext(challenge_id):
    '''Returns the ciphertext for the given challenge.'''
    if type(challenge_id) != int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")

    return challenge.ciphertext
    
def user_in_challenge(challenge_id, user):
    '''Returns True if the given user is registered in the given Challenge and False otherwise.'''
    if type(challenge_id) != int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")
        
    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")
        
    #success = challenge.user_set.filter(pk=user_id)
    success = user.user_challenge_set.get(pk=challenge_id)
    
    if success != None:
        return True
        
    else:
        return False
