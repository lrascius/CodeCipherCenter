#!cccenter/views.py
'''Holds the views for the cccenter app.'''
import json
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core.context_processors import csrf
import cccenter.python.general as general
import cccenter.python.cipher as cf
from random import randint
from cccenter.python.forms import RegistrationForm

def index(request):
    '''Returns the homepage.'''
    return render(request, 'cccenter/challenge_page.html', {"title":"Code and Cipher Center"})

# def register(request):
#     '''Returns the register page.'''
#     return render(request, 'cccenter/register.html')

def getCipher(request):
    '''Returns a ciphertext as JSON.'''
    cipher = {}
    text = general.generate_paragraph()
    cipher['text'] = text
    cipher['cipher'] = cf.ceasar_shift_encode(text, randint(2, 9))
    return HttpResponse(json.dumps(cipher['cipher']), content_type="application/json")

def login(request):
    '''Returns login page.'''
    c = {}
    c.update(csrf(request))
    return render_to_response('cccenter/login.html', c)

def auth_view(request):
    '''Authenticates user or returns error page is authentication fails.'''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return render_to_response('cccenter/login.html',
                                  RequestContext(request,
                                                 {"alert":"Invalid username or password!"}))

def loggedin(request):
    '''Returns challenge page.'''
    return render(request, 'cccenter/challenge_page.html')

def logout(request):
    '''Logs user out and returns challenge page.'''
    auth.logout(request)
    return render_to_response('cccenter/challenge_page.html')

def register(request):
    '''If called with a GET request, returns registration page.
       If called with a POST request, verifies user registration
       information. If valid, registers use. Else returns an error.'''
    registered = False

    if request.method == 'POST':

        user_form = RegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = RegistrationForm()

    return render(request,
                  'cccenter/register.html',
                  {'user_form': user_form, 'registered': registered})

