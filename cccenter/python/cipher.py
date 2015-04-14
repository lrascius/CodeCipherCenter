#!cccenter/python/cipher.py
'''Generates ciphertext objects.'''

from cccenter.models import *
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

def create_challenge(plaintext, ciphertext, ciphertype, key,
                     challenge_type, users = None, dt_created = None, dt_solved = None, solved_by = None):
            
    #raise Exception(users)
    
    if dt_created is not None:
        dt_created = dt_created
    else:
        dt_created = timezone.now()
                  
    challenge = Challenge.objects.create(plaintext = plaintext, ciphertext = ciphertext, ciphertype = ciphertype,
                                         cipherkey = key, challenge_type = challenge_type, datetime_created = dt_created)
                                         
    if users is not None:
        for user in users:
            challenge.users.add(user)
    
    if dt_solved is not None:
        challenge.datetime_solved = dt_solved
        
    if solved_by is not None:
        challenge.solved_by = solved_by
        
    challenge.save()
    
    return {'ciphertext':challenge.ciphertext, 'challenge_id':challenge.id}
