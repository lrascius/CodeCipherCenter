#!cccenter/python/cipher.py
'''
Interfaces with the Cipher model.
'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from cccenter.models import Cipher

def caesar_shift_encode(text, shift):
    '''
    Applies the Caesar Shift Cipher to the given ciphertext.

    :param text: The text to be encrypted
    :param shift: The Caesar Shift key
    :type text: str
    :type shift: int
    :return: The encrypted text, all upper case
    :rtype: str
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

    :param text: The text to be encrypted
    :param mult: The Multiplicitive Cipher multiplier key
    :type text: str
    :type mult: int
    :return: The encrypted text, all upper case
    :rtype: str

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

    :param text: The text to be encrypted
    :param a: The Affine Cipher multiplier key
    :param b: The Affine Cipher additive key
    :type text: str
    :type a: int
    :type b: int
    :return: The encrypted text, all upper case
    :rtype: str

    .. warning:: The affine cipher computes Cipher = (a*position + b) mod 26 and is invalid for\
    even values of a and when a is congruent to 13 mod 26
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

def check_solution(challenge_id, user_id, guessed_plaintext):
    '''
    Checks if the suggested solution is correct.

    :param challenge_id: The associated challenge's id
    :param user_id: The current user's id
    :param guessed_plaintext: The proposed solution to the challenge
    :type challenge_id: int
    :type user_id: int
    :type guessed_plaintext: str
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

    :param ciphertype: The cipher to apply to the text
    :param plaintext: The text to encrypt
    :type ciphertype: str
    :type plaintext: str
    :return: 'ciphertext' (str): The encrypted ciphertext (string)
    :return: 'cipherkey' (str): The cipher key (string)
    :rtype: dict

    .. warning:: Although ciphertype is a string, it must match one of the Cipher objects in the\
    database or it will throw an error.

    .. note:: The cipherkey is stored for display purposes only, so it is always stored as a string.
    '''

    if ciphertype == "Caesar Shift":
        cipherkey = randint(1, 25)
        ciphertext = caesar_shift_encode(plaintext, cipherkey)
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
