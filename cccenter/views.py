#!cccenter/views.py
'''Holds the views for the cccenter app.'''
import json
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
import cccenter.python.general as general
import cccenter.python.cipher as cf
from random import randint
from cccenter.python.forms import RegistrationForm
from django.contrib.auth.models import User, AnonymousUser
import cccenter.python.challenge as challenge

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

@login_required
def create_challenge(request):
    '''Creates a new challenge.'''
    if request.method == 'GET':
        return Http404()
        
    elif request.method == 'POST':
        cipher = {}
        cipher['plaintext'] = general.generate_paragraph()
        cipher['key'] = randint(1, 25)
        cipher['ciphertext'] = cf.ceasar_shift_encode(cipher['plaintext'], cipher['key'])
        cipher['ciphertype'] = "Caesar Shift Cipher"
        cipher['challenge_type'] = "single"
        cipher['users'] = [User.objects.get(pk=request.user.id)]

        cd = cf.create_challenge(cipher['plaintext'], cipher['ciphertext'], cipher['ciphertype'],
                                 cipher['key'], cipher['challenge_type'], cipher['users'])

        return HttpResponse(json.dumps(cd), content_type="application/json")
    
@login_required
def check_plaintext(request):
    '''Checks if submitted plaintext is the correct answer.  Returns True or False.'''
    if request.method == 'GET':
        return Http404()
    elif request.method == 'POST':
        challenge_id = int(request.POST.get("challenge_id", ""))
        user_id = request.user.id
        guessed_plaintext = request.POST.get("guessed_plaintext", "")
        success = cf.check_solution(challenge_id, user_id, guessed_plaintext)
    
        return HttpResponse(json.dumps({'success':success}), content_type="application/json")
    
def challenge_page(request):
    '''Returns the challenge page associated with the given challenge_id.'''
    if request.method == 'POST':
        return Http404()
        
    elif request.method == 'GET':
        challenge_id = int(request.GET.get('challenge_id', ''))
        ct = challenge.get_ciphertext(challenge_id)
        c = {"title":"Code and Cipher Center", "challenge_id":challenge_id, "ciphertext":ct}
        c.update(csrf(request))
        return render(request, 'cccenter/challenge_page.html', c)

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

def challengeList(request):
    '''Returns challenge list'''
    return render(request, 'cccenter/challenge_list.html')

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

@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user=request.user)

    return render(request, 
                  'cccenter/profile.html',
                   {'user' : user, 'userprofile' : userprofile})




