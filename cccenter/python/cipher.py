#!cccenter/python/cipher.py
'''Handles primary references to ciphertext objects.'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from cccenter.models import Cipher

def ceasar_shift_encode(text, shift):
    '''
    Applies the Caesar Shift Cipher to the given ciphertext.
    
    :param text: the text to be encrypted
    :param shift: the Caesar Shift key
    :type text: string
    :type shift: int
    :return: the encrypted text, all upper case
    :rtype: string
    '''
    # List of 26 lowercase letters
    alphabet = list(map(chr, range(97, 123)))

    encoded_text = ""
    text = "".join(text.lower().split())
    for char in text:
        if char in alphabet:
            char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            encoded_text += char
    return encoded_text.upper()

def multiplicitive_cipher(text, mult):
    '''
    Applies the Multiplicitive Shift Cipher to a piece of text.
    
    :param text: the text to be encrypted
    :param mult: the Multiplicitive Cipher multiplier key
    :type text: string
    :type mult: int
    :return: the encrypted text, all upper case
    :rtype: string
    
    .. warning:: Cipher = (mult * position) mod 26 and is invalid for even multiples
    '''
    # List of 26 lowercase letters
    if mult % 2 == 0:
        raise Exception("Even key is invalid for a multiplicitive cipher")

    alphabet = list(map(chr, range(97, 123)))

    encoded_text = ""
    text = "".join(text.lower().split())
    for char in text:
        if char in alphabet:
            char = alphabet[(((alphabet.index(char)+1) * mult) % len(alphabet)) - 1]
            encoded_text += char
    return encoded_text.upper()

def affine_cipher(text, a, b):
    '''
    Applies the Affine Cipher on a piece of text.
    
    :param text: the text to be encrypted
    :param a: the Affine Cipher multiplier key
    :param b: the Affine Cipher additive key
    :type text: string
    :type a: int
    :type b: int
    :return: the encrypted text, all upper case
    :rtype: string
    
    .. warning:: The affine cipher computes Cipher = (a*position + b) mod 26 and is invalid for even\
    values of a and when a is congruent to 13 mod 26
    '''
    # List of 26 lowercase letters
    if a % 2 == 0 or a % 13 == 0:
        raise Exception("Invalid value for a in affine cipher")

    alphabet = list(map(chr, range(97, 123)))

    encoded_text = ""
    text = "".join(text.lower().split())
    for char in text:
        if char in alphabet:
            char = alphabet[((((alphabet.index(char)+1) * a) + b) % len(alphabet)) - 1]
            encoded_text += char
    return encoded_text.upper()

def create_challenge(plaintext, ciphertext, ciphertype, key, challenge_type,
                     users=None, dt_created=None, solved=False, dt_solved=None, solved_by=None):
    '''
    Creates a challenge object and puts it in the database.
    
    :param plaintext: the associated plaintext
    :param ciphertext: the associate ciphertext
    :param ciphertype: the cipher the challenge uses
    :param key: the cipher's key
    :param challenge_type: the type of challenge (single, collaborative, competitive)
    :param users: (optional) the users registered in the challenge
    :param dt_created: (optional) the date and time the challenge was created
    :param solved: (optional) indicates if the challenge has been solved yet
    :param dt_solved: (optional) the date and time the challenge was first solved
    :param solved_by: (optional) the users who have already solved the challenge
    :type plaintext: string
    :type cipehrtext: string
    :type ciphertype: string
    :type key: string
    :type challenge_type: string
    :type users: [User]
    :type dt_created: datetime
    :type solved: boolean
    :type dt_solved: datetime
    :type solved_by: [User]
    :return: 'ciphertext': the ciphertext associated with the challenge
    :return: 'challenge_id': the challenge's id
    :rtype: dict
    
    .. note:: The key is a string and is only recorded for future reference. The plaintext\
    and ciphertext are used to print the challenge and check proposed solutions.
    
    .. note:: If dt_created is left unassigned, the current date and time are used. This is the best default option.
    
    .. warning:: Although ciphertype and challenge_type are strings, they are used to pull the correct\
    Cipher object and challenge_type from the database and therefore must match a database entry exactly.
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

def check_solution(challenge_id, user_id, guessed_plaintext):
    '''
    Checks if the suggested solution is correct.
    
    :param challenge_id: the associated challenge's id
    :param user_id: the current user's id
    :param guessed_plaintext: the proposed solution to the challenge
    :type challenge_id: int
    :type user_id: int
    :type guessed_plaintext: string
    :return: True if the proposed solution is correct, false if it is not
    :rtype: boolean
    
    .. warning:: If the challenge_id or user_id is not valid, will throw an error.
    
    .. warning:: Does not check if the user is registered in the challenge before checking that\
    the solution is correct.
    '''
    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    if isinstance(user_id, int) == False:
        raise TypeError("user_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("challenge_id is not valid")

    user = User.objects.get(pk=user_id)

    if user == None:
        raise ValueError("user_id is not valid")

    if challenge.plaintext == guessed_plaintext:
        # if challenge has not already been solved
        u_s = challenge.solved_by.all()
        if not user in u_s:
            challenge.solved_by.add(user)

        if challenge.solved == False or challenge.solved == None:
            challenge.solved = True
            challenge.datetime_solved = timezone.now()
            challenge.save()

        return True

    else:
        return False

def create_ciphertext(ciphertype, plaintext):
    '''
    Returns a ciphertext and key using the given ciphertype.
    
    :param ciphertype: the cipher to apply to the text
    :param plaintext: the text to encrypt
    :type ciphertype: string
    :type plaintext: string
    :return: 'ciphertext': the encrypted ciphertext (string)
    :return: 'cipherkey': the cipher key (string)
    :rtype: dict
    
    .. warning:: Although ciphertype is a string, it must match one of the Cipher objects in the database\
    or it will throw an error.
    '''
    
    if ciphertype == "Caesar Shift":
        cipherkey = randint(1, 25)
        ciphertext = ceasar_shift_encode(plaintext, cipherkey)
        return {'ciphertext':ciphertext, 'cipherkey':cipherkey}

    if ciphertype == "Multiplicitive":
        cipherkey = randint(2, 1000)
        while cipherkey % 2 == 0 or cipherkey % 26 == 1:
            cipherkey = randint(2, 1000)
        ciphertext = multiplicitive_cipher(plaintext, cipherkey)
        return {'ciphertext':ciphertext, 'cipherkey':cipherkey}

    if ciphertype == "Affine Cipher":
        a = randint(1, 1000)
        while a % 2 == 0 or a % 13 == 0:
            a = randint(1, 1000)
        b = randint(1, 1000)
        cipherkey = "a: " + str(a) + " b: " + str(b)
        ciphertext = affine_cipher(plaintext, a, b)
        return {'ciphertext':ciphertext, 'cipherkey':cipherkey}
