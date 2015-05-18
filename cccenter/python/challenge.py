#!cccenter/python/challenge.py
'''
Interfaces with the Challenge model.
'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone
from cccenter.models import Cipher

def create_challenge(plaintext, ciphertext, ciphertype, key, challenge_type,
                     users=None, dt_created=None, solved=False, dt_solved=None, solved_by=None):
    '''
    Creates a challenge object and puts it in the database.

    :param plaintext: The associated plaintext
    :param ciphertext: The associate ciphertext
    :param ciphertype: The cipher the challenge uses
    :param key: The cipher's key
    :param challenge_type: The type of challenge (single, collaborative, competitive)
    :param users: (optional) Users registered in the challenge
    :param dt_created: (optional) The date and time the challenge was created
    :param solved: (optional) Indicates if the challenge has been solved yet
    :param dt_solved: (optional) The date and time the challenge was first solved
    :param solved_by: (optional) Users who have already solved the challenge
    :type plaintext: str
    :type cipehrtext: str
    :type ciphertype: str
    :type key: str
    :type challenge_type: str
    :type users: [models.User]
    :type dt_created: datetime
    :type solved: boolean
    :type dt_solved: datetime
    :type solved_by: [models.User]
    :return: 'ciphertext' (str): The ciphertext associated with the challenge
    :return: 'challenge_id' (int): The challenge's id
    :rtype: dict

    .. note:: The key is a string and is only recorded for future reference. The plaintext\
    and ciphertext are used to print the challenge and check proposed solutions.

    .. note:: If dt_created is left unassigned, the current date and time are used. This is the\
    best default option.

    .. warning:: Although ciphertype and challenge_type are strings, they are used to pull the\
    correct Cipher object and challenge_type from the database and therefore must match a\
    database entry exactly.
    '''

    if dt_created != None:
        dt_created = dt_created
    else:
        dt_created = timezone.now()

    challenge = models.Challenge.objects.create(plaintext=plaintext, ciphertext=ciphertext,
                                                ciphertype=ciphertype, cipherkey=key,
                                                challenge_type=challenge_type,
                                                datetime_created=dt_created)

    cipher = Cipher.objects.get(ciphertype=ciphertype)
    challenge.cipher.add(cipher)

    if users != None:
        for user in users:
            challenge.users.add(user)

    if solved != None:
        if solved is True:
            challenge.solved = True

            if dt_solved is not None:
                challenge.datetime_solved = dt_solved
            else:
                raise ValueError("Null value passed for datetime solved when solved is True")

            if solved_by is not None:
                for suser in solved_by:
                    challenge.solved_by.add(suser)
            else:
                raise ValueError("Null value passed for solved_by solved when solved is True")

    challenge.save()

    return {'ciphertext':challenge.ciphertext, 'challenge_id':challenge.id}

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

    .. note:: Practically, this function will only return False when the challenge type is\
    'single', since users are note allowed to be added to a private challenge.
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
    Determines if the user is registered in the challenge and if the user already\
    solved the challenge.

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
    Returns the difficulty of the given challenge. If multiple ciphers have been applied,\
    returns the hardest one.

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
    :return: 'datetime_created' (datetime): The date and time the challenge was created
    :return: 'datetime_solved' (datetime): The date and time the challenge was first solved
    :return: 'challenge_type' (str): The type of challenge (single, competitive, or collaborative)
    :return: 'solved_by' ([models.User]): Who has solved the challenge
    :return: 'users' ([models.User]): Who is registered in the challenge
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
