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
import cccenter.python.comment as comment
from random import randint
from cccenter.models import UserProfile
from cccenter.models import Cipher
from cccenter.models import Challenge
from cccenter.models import Notification
from cccenter.python.forms import RegistrationForm
from cccenter.python.forms import SettingsForm
from django.contrib.auth.models import User, AnonymousUser
import cccenter.python.challenge as challenge
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
    '''Returns the homepage.'''
    return render(request, 'cccenter/home_page.html',
                  {"title":"Code and Cipher Center", 
                   "active":"home"})


def update_notifications(request):
    '''Udates the notifications based on which has been viewed'''
    print request.user
    general.viewed_notification(request.user, request.GET.get('notification_id'))

def home(request):
    '''Returns the home page.'''
    return render(request, 'cccenter/challenge_page.html',
		          {"title":"Code and Cipher Center"})

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
    '''Creates a new challenge
       If a difficulty was selected we pick a random cipher based on the difficulty
       Else we create a cipher based on what the user chose.'''

    if request.method == 'GET':
        return render(request, 'cccenter/create_challenge.html', {"title":"Code and Cipher Center", 
                                                                  "active":"newchallenge",
                                                                  "notifications" : general.get_notifications(request.user),
                                                                  "unseen_notification" : general.unviewed_notifications(request.user)})

    elif request.method == 'POST':
        if len(request.POST.getlist('challengetype')) == 0:
            return render(request, 'cccenter/create_challenge.html', {"title":"Code and Cipher Center", "active":"newchallenge",
                                                                      "bool":True, "error":"Challenge type is required",
                                                                      "notifications" : general.get_notifications(request.user),
                                                                      "unseen_notification" : general.unviewed_notifications(request.user)})
        if len(request.POST.getlist('radiogroup')) == 0 and len(request.POST.getlist('cipher')) == 0:
            return render(request, 'cccenter/create_challenge.html', {"title":"Code and Cipher Center", "active":"newchallenge",
                                                                      "bool":True,
                                                                      "error":"Select by difficulty or list of ciphers",
                                                                      "notifications" : general.get_notifications(request.user),
                                                                      "unseen_notification" : general.unviewed_notifications(request.user)})
        cipher = {}
        cipher['plaintext'] = general.generate_paragraph()
        if len(request.POST.getlist('radiogroup')) != 0:
            difficulty_ciphers = [i.ciphertype for i in Cipher.objects.all().filter(difficulty=request.POST.getlist('radiogroup')[0])]
            cipher['ciphertype'] = difficulty_ciphers[randint(0, len(difficulty_ciphers)-1)]
        else:
            cipher['ciphertype'] = request.POST.getlist('cipher')[0]
        ciphertext = cf.create_ciphertext(cipher['ciphertype'], cipher['plaintext'])

        cipher['key'] = ciphertext['cipherkey']
        cipher['ciphertext'] = ciphertext['ciphertext']
        cipher['challenge_type'] = request.POST.getlist('challengetype')[0]
        cipher['users'] = [User.objects.get(pk=request.user.id)]

        cd = cf.create_challenge(cipher['plaintext'], cipher['ciphertext'], cipher['ciphertype'],
                                 cipher['key'], cipher['challenge_type'], cipher['users'])

        #return HttpResponse(json.dumps(cd), content_type="application/json")
        return HttpResponseRedirect('/cipher/challengepage/?challenge_id='
                                    +str(cd['challenge_id']))#, {'challenge_id':cd['challenge_id']})

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
        link = "/cipher/challengepage/?challenge_id=" + str(request.GET.getlist('challenge_id')[0]) 
        notify = str(request.user) + " has invited you to a challenge"
        user = User.objects.get(username = request.POST.getlist('username')[0])        
        notification = Notification(user=user, notification=notify, link=link)
        notification.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return render(request, 'cccenter/challenge_page.html', {"notifications" : general.get_notifications(request.user),
                                                                # "unseen_notification" : general.unviewed_notifications(request.user) })

    elif request.method == 'GET':
        challenge_id = int(request.GET.get('challenge_id', ''))
        ct = challenge.get_ciphertext(challenge_id)
        in_challenge, solved_by_user = challenge.user_in_challenge(challenge_id, request.user)
        info = challenge.get_challenge_info(challenge_id)

        difficulty = challenge.get_difficulty(challenge_id)
        c = {"title":"Code and Cipher Center", "challenge_id":challenge_id,
             "ciphertext":ct, "user_in_challenge":in_challenge, "difficulty":difficulty,
             "challenge_type":info['challenge_type'], "solved":info['solved'],
             "num_users":len(info['users']), "num_solved":len(info['solved_by']),
             "users": info['users'], "solved_by":info['solved_by'], "solved_by_user":solved_by_user,
             "notifications" : general.get_notifications(request.user),
             "unseen_notification" : general.unviewed_notifications(request.user)}

        if info['challenge_type'] == 'collaborative':
            cmts = comment.get_comments(challenge_id)
            c['comments'] = cmts

        c.update(csrf(request))
        return render(request, 'cccenter/challenge_page.html', c)

@login_required
def join_challenge(request):
    '''Adds the current user to the returned challenge.'''
    if request.method == 'GET':
        return Http404()

    elif request.method == 'POST':
        challenge_id = int(request.POST.get('challenge_id', ''))
        #raise Exception(challenge_id)
        challenge.join_challenge(challenge_id=challenge_id, user_id=request.user.id)
        #return HttpResponseRedirect('/cipher/challengepage/', {'challenge_id':challenge_id})
        return HttpResponseRedirect('/cipher/challengepage/?challenge_id='+str(challenge_id))

def login(request):
    '''Returns login page.'''
    c = {"active":"login", 
         "title":"Code and Cipher Center"}
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
                                                 {"alert":"Invalid username or password!", 
                                                  "title":"Code and Cipher Center",
                                                  "notifications" : general.get_notifications(request.user),
                                                  "unseen_notification" : general.unviewed_notifications(request.user)}))

def challengeList(request):
    '''Returns challenge list with collumns of id, date, difficulty, and challengetype'''
    challenges = Challenge.objects.all()
    challenges_of_user = Challenge.objects.filter(users=request.user)
    c = []
    difficulty = []
    challenge_type = []
    for challenge in challenges_of_user:
        c.append(challenge.id)
    for chall in challenges:
        difficulty.append(Cipher.objects.get(ciphertype=chall.ciphertype).difficulty.capitalize())
        challenge_type.append(chall.challenge_type.capitalize())
    array = zip(challenges, difficulty, challenge_type)

    return render(request, 'cccenter/challenge_list.html', {'in_challenge':c, 
                                                            'list':array, 
                                                            "title":"Code and Cipher Center", 
                                                            "active":"challengelist",
                                                            "notifications" : general.get_notifications(request.user),
                                                            "unseen_notification" : general.unviewed_notifications(request.user)})

def loggedin(request):
    '''Returns challenge page.'''
    return render(request, 'cccenter/challenge_page.html', {"active":"challenge", 
                                                            "title":"Code and Cipher Center", 
                                                            "notifications" : general.get_notifications(request.user),
                                                            "unseen_notification" : general.unviewed_notifications(request.user)})

@login_required
def logout(request):
    '''Logs user out and returns challenge page.'''
    auth.logout(request)
    return render_to_response('cccenter/challenge_page.html', {"title":"Code and Cipher Center"})

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
                  {'user_form': user_form, 
                   'registered': registered, 
                   "active":"register", 
                   "title":"Code and Cipher Center"})

@login_required
def profile(request):
    '''Get the user information, and if the profile does not exist create one
       Render the page with the user and user profile information'''
    user = User.objects.get(username=request.user)
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user=request.user)

    difficulty = []
    # challenges = Challenge.objects.all()
    challenges_user_in = Challenge.objects.filter(users=request.user)
    for challenge in challenges_user_in:
        difficulty.append(Cipher.objects.get(ciphertype=challenge.ciphertype).difficulty.capitalize())
    array = zip(challenges_user_in, difficulty)
    # c = []
    # difficulty = []
    # challenge_type = []
    # for challenge in challenges_of_user:
    #     c.append(challenge.id)

    # for challenge in challenges:
    #     if(challenge.id in challenges_id):
    #         challenges_user_in.append(challenge)

    # array = zip(challenges, difficulty, challenge_type)

    # for chall in challenges:
    #     difficulty.append(Cipher.objects.get(ciphertype=chall.ciphertype).difficulty.capitalize())
    #     challenge_type.append(chall.challenge_type.capitalize())

    return render(request,
                  'cccenter/profile.html',
                  {'user':user, 
                   'userprofile':userprofile, 
                   'challenges_user_in':array, 
                   "title":"Code and Cipher Center", 
                   "notifications" : general.get_notifications(request.user),
                   "unseen_notification" : general.unviewed_notifications(request.user)})

@login_required
def settings(request):
    '''Try getting the user profile, if it does not exists create one.
       If called with a GET request, returns settings page.
       If called with POST, create a settings, user, and password forms.
       Update all the corresponding tables and return the profile page'''
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, request.FILES, instance=profile)
        #user_form = RegistrationForm(data=request.POST)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)

        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        if settings_form.is_valid():
            settings_form.save()

        return HttpResponseRedirect('/profile/')

    return render(request, 'cccenter/settings.html', {"title":"Code and Cipher Center", 
                                                      "notifications" : general.get_notifications(request.user),
                                                      "unseen_notification" : general.unviewed_notifications(request.user)})

