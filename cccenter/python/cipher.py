#!cccenter/python/cipher.py
'''Generates ciphertext objects.'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from cccenter.models import Cipher

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
    '''Function that applies a multiplicitive shift on a piece of text. The
       encrypted text is returned. The multiplicitive cipher computes
       Cipher = (mult * position) mod 26 and is invalid for even multiples'''
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
    '''Function that applies a affine cipher on a piece of text. The encrypted text
       is returned. The affine cipher computes Cipher = (a*position + b) mod 26 and
       is invalid for even values of a and when a is congruent to 13 mod 26'''
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
    '''Creates a challenge object and puts it in the database.'''

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
                challenge.solved_by = solved_by
            else:
                raise ValueError("Null value passed for solved_by solved when solved is True")

    challenge.save()

    return {'ciphertext':challenge.ciphertext, 'challenge_id':challenge.id}

def check_solution(challenge_id, user_id, guessed_plaintext):
    '''Checks if the suggested solution is correct.'''
    if type(challenge_id) is not int:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    if type(user_id) is not int:
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
    '''Function that returns a ciphertext and a key based on the
       particular ciphertype'''
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
