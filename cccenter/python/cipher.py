#!cccenter/python/cipher.py
'''Generates ciphertext objects.'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone

def ceasar_shift_encode(text, shift):
    '''Function that applies a ceasar shift on a piece of text. The encrypted text is returned.'''
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
    '''Function that applies a multiplicitive shift on a piece of text. The encrypted text is returned.'''
    # List of 26 lowercase letters
    if(mult % 2 == 0):
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
    '''Function that applies a affine cipher on a piece of text. The encrypted text is returned.'''
    # List of 26 lowercase letters
    if(a % 2 == 0 or a % 13 == 0):
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
    '''Creates a challenge object and puts it in the database.'''

    if dt_created is not None:
        dt_created = dt_created
    else:
        dt_created = timezone.now()

    challenge = models.Challenge.objects.create(plaintext=plaintext, ciphertext=ciphertext,
                                         ciphertype=ciphertype, cipherkey=key,
                                         challenge_type=challenge_type, datetime_created=dt_created)

    if users is not None:
        for user in users:
            challenge.users.add(user)
            
    if solved is not None:
        if solved is True:
            challenge.solved = True

            if dt_solved is not None:
                challenge.datetime_solved = dt_solved
            else:
                raise ValueError("Null value passed for datetime solved when solved is True")

            if solved_by is not None:
                challenge.solved_by = solved_by
            else:
                raise ValueError("Null value passed for solved_by solved when solved is True")

    challenge.save()

    return {'ciphertext':challenge.ciphertext, 'challenge_id':challenge.id}
    
def check_solution(challenge_id, user_id, guessed_plaintext):
    if type(challenge_id) is not int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")
    
    if type(user_id) is not int:
        raise TypeError("user_id is " + str(type(challenge_id)) + ", not int")
    
    challenge = models.Challenge.objects.get(pk=challenge_id)
    
    if challenge is None:
        raise ValueError("challenge_id is not valid")
        
    user = User.objects.get(pk=user_id)
    
    if user is None:
        raise ValueError("user_id is not valid")
        
    if challenge.plaintext == guessed_plaintext:
        # if challenge has not already been solved
        if challenge.solved == False or challenge.solved == None:
            challenge.solved = True
            challenge.solved_by = user
            challenge.datetime_solved = timezone.now()
            challenge.save()
        
        return True
        
    else:
        return False

