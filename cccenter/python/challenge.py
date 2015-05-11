#!cccenter/python/challenge.py
'''
Interfaces with the Challenge model.
'''

import cccenter.models as models
from django.contrib.auth.models import User

def challenge_list():
    '''
    Returns a list of the challenges in the database.
    
    :return: All challenge objects in the database
    :rtype: [models.Challenge]
    
    .. note:: Actually returns a queryset containing all challenges but can be treated as an arry.
    '''
    chList = models.Challenge.objects.all()

    return chList

def join_challenge(challenge_id, user_id):
    '''
    Adds the given user to the given challenge.
    
    :param challenge_id: The challenge's associated object's id number
    :param user_id: The user's (user object's) id number
    :type challenge_id: int
    :type user_id: int
    :return: Returns True if the user is added successfully. Returns False otherwise.
    :rtype: boolean
    
    .. note:: Practically, this function will only return False when the challenge type is 'single',\
    since users are note allowed to be added to a private challenge.
    '''
    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    if isinstance(user_id, int) == False:
        raise TypeError("user_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("challenge_id is invalid")

    if challenge.challenge_type == 'single':
        return False

    user = User.objects.get(pk=user_id)

    if user == None:
        raise ValueError("user_id is invalid")

    challenge.users.add(user)
    challenge.save()
    return True

def get_ciphertext(challenge_id):
    '''
    Returns the ciphertext associated with the given challenge.
    
    :param challenge_id: The challenge's associated object's id number
    :type challenge_id: int
    :return: The ciphertext associated with the challenge
    :rtype: str
    '''
    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")

    return challenge.ciphertext

def user_in_challenge(challenge_id, user):
    '''
    Determines if the user is registered in the challenge and if the user already solved the challenge.
    
    :param challenge_id: The challenge's associated object's id number
    :param user: The current user
    :type challenge_id: int
    :type user: models.User
    :return: (User in the challenge, User solved the challenge)
    :rtype: (boolean, boolean)
    
    .. note:: The user parameter can be passed in easily from a view using request.user.
    '''

    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")

    #success = challenge.user_set.filter(pk=user_id)
    try:
        success = user.user_challenge_set.get(pk=challenge_id)
    except:
        return False, False

    if success == None:
        return False, False
    else:
        if user.user_solved_challenge_set.filter(pk=challenge_id).exists():
            return True, True
        else:
            return True, False

def get_difficulty(challenge_id):
    '''
    Returns the difficulty of the given challenge. If multiple ciphers have been applied, returns the hardest one.
    
    :param challenge_id: The challenge's associated object's id number
    :type challenge_id: int
    :return: The difficulty of the challenge
    :rtype: str
    
    .. note:: Return values can include 'beginner', 'intermediate', and 'advanced'.
    
    .. note:: Although this function supports multiple ciphers being applied to a single challenge,\
    the rest of the code, including the models, does not.
    '''

    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    ciphers = challenge.cipher.all()
    difficulties = [i.difficulty for i in ciphers]

    if 'advanced' in difficulties:
        return 'advanced'
    elif 'intermediate' in difficulties:
        return 'intermediate'
    else:
        return 'beginner'

def get_challenge_info(challenge_id):
    '''
    Returns information about the Challenge to display on the challenge page.
    
    :param challenge_id: The challenge's associated object's id number
    :type challenge_id: int
    :return: 'datetime_created' (datetime): the date and time the challenge was created
    :return: 'datetime_solved' (datetime): the date and time the challenge was first solved
    :return: 'challenge_type' (str): the type of challenge (single, competitive, or collaborative)
    :return: 'solved_by' ([models.User]): who solved the challenge
    :return: 'users' ([models.User]): who is registered in the challenge
    :rtype: dict
    
    .. note:: the 'solved_by' and 'user' indices of the returned dictionary are actually\
    query sets, but can be treated as lists.
    '''

    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    res = {}
    res['datetime_created'] = challenge.datetime_created
    res['datetime_solved'] = challenge.datetime_solved
    res['challenge_type'] = challenge.challenge_type
    res['solved_by'] = challenge.solved_by.all()
    res['solved'] = challenge.solved
    res['users'] = challenge.users.all()

    return res
