#!cccenter/views.py
'''Holds the views for the cccenter app.'''
import json
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse
import cccenter.python.general as general
import cccenter.python.cipher as cf
from random import randint

def index(request):
    '''Returns the homepage.'''
    #return HttpResponse("Hello, World!") # should really return the homepage
    return render(request, 'cccenter/challenge_page.html', {"title":"Code and Cipher Center"})

def register(request):
    '''Returns the register page.'''
    return render(request, 'cccenter/register.html')

def getCipher(request):
    '''Returns a ciphertext as JSON.'''
    cipher = {}
    text = general.generate_paragraph()
    cipher['text'] = text
    cipher['cipher'] = cf.ceasar_shift_encode(text, randint(2, 9))
    return HttpResponse(json.dumps(cipher['cipher']), content_type="application/json")
