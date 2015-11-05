#!cccenter/views.py
'''
Holds the views for the cccenter app.
'''

import json
from django import shortcuts
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core import context_processors
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core import mail
import cccenter.python.general as general
import cccenter.python.notification as notify
import cccenter.python.cipher as cf
import cccenter.python.comment as comment
import cccenter.python.challenge as challenge
import random
from cccenter.models import UserProfile
from cccenter.models import Cipher
from cccenter.models import Challenge
from cccenter.models import Notification
from cccenter.models import Comment
from cccenter.python.forms import RegistrationForm
from cccenter.python.forms import SettingsForm
from django.contrib.auth.models import User
import cccenter.python.challenge as challenge
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q

def update_notifications(request):
    '''Updates the notifications based on which has been viewed'''
    notify.viewed_notification(request.user, request.GET.get('notification_id'))

def home(request):
    '''Returns the home page.'''

    context = {"title":"Code and Cipher Center",
               "active":"home"}

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')

        if subject and message and email:
            mail.send_mail(subject, message, email, ['mkurtz00@citymail.cuny.edu'])
            mail.send_mail(subject, message, email, ['admin@cccenter.com'])
            context['message'] = 'Thank you, your message has been sent.'

        else:
            context['message'] = 'Please make sure all fields are filled.'

    if not request.user.is_anonymous():
        context["notifications"] = notify.get_notifications(request.user, False)
        context["unseen_notification"] = notify.unviewed_notifications(request.user)

    return shortcuts.render(request, 'cccenter/home_page.html', context)

def getCipher(request):
    '''Returns a ciphertext as JSON data.'''
    cipher = {}
    text = general.generate_paragraph()
    cipher['text'] = text
    cipher['cipher'] = cf.caesar_shift_encode(text, random.randint(2, 9))
    return HttpResponse(json.dumps(cipher['cipher']), content_type="application/json")

@login_required
def create_challenge(request):
    '''
    A page used to create a new challenge.
    If called with a GET request, returns the page. If called with a POST request,
    creates the challenge.
    If a difficulty was selected we pick a random cipher based on the difficulty
    Else we use the selected cipher.
    '''

    if request.method == 'GET':
        return shortcuts.render(request, 'cccenter/create_challenge.html',
                                {"title":"Code and Cipher Center", "active":"newchallenge",
                                 "notifications" : notify.get_notifications(request.user, False),
                                 "unseen_notification" : notify.unviewed_notifications(request.user)
                                })

    elif request.method == 'POST':
        if len(request.POST.getlist('challengetype')) == 0:
            return shortcuts.render(request, 'cccenter/create_challenge.html',
                                    {"title":"Code and Cipher Center", "active":"newchallenge",
                                     "bool":True, "error":"Challenge type is required",
                                     "notifications":notify.get_notifications(request.user, False),
                                     "unseen_notification":notify.unviewed_notifications(request.user)
                                    })

        if len(request.POST.getlist('radiogroup')) == 0 \
           and len(request.POST.getlist('cipher')) == 0:
            return shortcuts.render(request, 'cccenter/create_challenge.html',
                                    {"title":"Code and Cipher Center", "active":"newchallenge",
                                     "bool":True, "error":"Select by difficulty or list of ciphers",
                                     "notifications":notify.get_notifications(request.user, False),
                                     "unseen_notification":notify.unviewed_notifications(request.user)
                                    })
        cipher = {}
        cipher['plaintext'] = general.generate_paragraph()
        if len(request.POST.getlist('radiogroup')) != 0:
            difficulty_ciphers = [i.ciphertype for i in Cipher.objects.all().filter(difficulty=request.POST.getlist('radiogroup')[0])]
            cipher['ciphertype'] = difficulty_ciphers[random.randint(0, len(difficulty_ciphers)-1)]
        else:
            cipher['ciphertype'] = request.POST.getlist('cipher')[0]
        ciphertext = cf.create_ciphertext(cipher['ciphertype'], cipher['plaintext'])

        cipher['key'] = ciphertext['cipherkey']
        cipher['ciphertext'] = ciphertext['ciphertext']
        cipher['challenge_type'] = request.POST.getlist('challengetype')[0]
        cipher['users'] = [User.objects.get(pk=request.user.id)]

        cd = challenge.create_challenge(cipher['plaintext'], cipher['ciphertext'], cipher['ciphertype'],
                                 cipher['key'], cipher['challenge_type'], cipher['users'])

        #return HttpResponse(json.dumps(cd), content_type="application/json")
        return HttpResponseRedirect('/cipher/challengepage/?challenge_id=' + str(cd['challenge_id']))

@login_required
def check_plaintext(request):
    '''
    Checks if submitted plaintext is the correct answer.
    If it is, update the challenge as solved by the user and return True.
    Else return false.
    '''
    if request.method == 'GET':
        return Http404()

    elif request.method == 'POST':
        challenge_id = int(request.POST.get("challenge_id", ""))
        user_id = request.user.id
        guessed_plaintext = request.POST.get("guessed_plaintext", "")
        success = cf.check_solution(challenge_id, user_id, guessed_plaintext)

        if success == True:
            notify.solved_cipher_notification(request.user.username, challenge_id)

        return HttpResponse(json.dumps({'success':success}), content_type="application/json")

def challenge_page(request):
    '''
    If requested with a GET request,
    Returns the challenge page associated with the given challenge_id.

    If requested with a POST request,
    Generates an invitation to the submitted user to join the challenge.
    '''
    if request.method == 'POST':
        if str(request.user.username) != str(request.POST.getlist('username')[0]):
            link = "/cipher/challengepage/?challenge_id="+str(request.GET.getlist('challenge_id')[0])
            notify_message = str(request.user.username) + " has invited you to a challenge # "\
                             + str(request.GET.getlist('challenge_id')[0])
            user = User.objects.get(username=request.POST.getlist('username')[0])
            notification = Notification(user=user, notification=notify_message,
                                        link=link, datetime=timezone.now())
            notification.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
             "users": info['users'], "solved_by":info['solved_by'], "solved_by_user":solved_by_user}

        if not request.user.is_anonymous():
            c["notifications"] = notify.get_notifications(request.user, False)
            c["unseen_notification"] = notify.unviewed_notifications(request.user)

        if info['challenge_type'] == 'collaborative':
            cmts = comment.get_comments(challenge_id)
            c['comments'] = cmts

        c.update(context_processors.csrf(request))
        return shortcuts.render(request, 'cccenter/challenge_page.html', c)

@login_required
def join_challenge(request):
    '''Adds the current user to the requested challenge.'''
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
    c.update(context_processors.csrf(request))
    return shortcuts.render_to_response('cccenter/login.html', c)

def auth_view(request):
    '''Authenticates user or returns error page if authentication fails.'''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')

    return shortcuts.render_to_response('cccenter/login.html',
                                        RequestContext(request,
                                                       {"alert":"Invalid username or password!",
                                                        "title":"Code and Cipher Center"
                                                       }
                                                      ))

def challengeList(request):
    '''
    Returns challenge list with collumns of id, date, difficulty, and challengetype.

    If the user is logged in, returns a list of his private challenges as well as all group\
    challenges.
    Else returns only a list of all group challenges.
    '''

    c = []

    if request.user.is_active:
        query = Q(users__in=[request.user]) | Q(challenge_type='collaborative')\
                | Q(challenge_type='competitive')
        challenges_of_user = Challenge.objects.filter(query).distinct()

        in_challenge = Challenge.objects.filter(Q(users__in=[request.user]))

        for challenge in in_challenge:
            c.append(challenge.id)

    else:
        challenges_of_user = Challenge.objects.exclude(challenge_type='single')

    difficulty = []
    challenge_type = []

    for chall in challenges_of_user:
        difficulty.append(Cipher.objects.get(ciphertype=chall.ciphertype).difficulty.capitalize())
        challenge_type.append(chall.challenge_type.capitalize())
    array = zip(challenges_of_user, difficulty, challenge_type)

    context = {"in_challenge":c,
               "list":array,
               "title":"Code and Cipher Center",
               "active":"challengelist"
              }

    if not request.user.is_anonymous():
        context["notifications"] = notify.get_notifications(request.user, False)
        context["unseen_notification"] = notify.unviewed_notifications(request.user)

    return shortcuts.render(request, 'cccenter/challenge_list.html', context)

def loggedin(request):
    '''Redirects to home page.'''
    return HttpResponseRedirect('/cccenter/challenge_page')

def usercomment(request):
    '''Adds a comment by updating the database
       Returns user to the challenge page
    '''
    if request.method == 'POST':
        challenge_id = int(request.GET.getlist('challenge_id')[0])

        comment = Comment.objects.create(forum_id=challenge_id,
                                         user=request.user, 
                                         text=request.POST.get('comment', ''),
                                         datetime=timezone.now())
    return HttpResponseRedirect('/cipher/challengepage/?challenge_id='+str(challenge_id))

@login_required
def logout(request):
    '''Logs user out and redirects to the home page.'''
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    '''
    If called with a GET request, returns registration page.

    If called with a POST request, verifies user registration information.
    If valid, registers use. Else returns an error.
    '''
    registered = False

    if request.method == 'POST':

        user_form = RegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.save()
            registered = True
        else:
            return Http404()
    else:
        user_form = RegistrationForm()

    return shortcuts.render(request,
                            'cccenter/register.html',
                            {'user_form': user_form,
                             'registered': registered,
                             "active":"register",
                             "title":"Code and Cipher Center"
                            }
                           )

@login_required
def profile(request):
    '''
    Returns the current user's profile page.

    If the user doesn't have an associated UserProfile, creates one.
    '''
    user = User.objects.get(username=request.user)
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user=request.user)

    difficulty = []

    challenges_user_in = Challenge.objects.filter(users=request.user)
    for challenge in challenges_user_in:
        cipher = Cipher.objects.get(ciphertype=challenge.ciphertype)
        difficulty.append(cipher.difficulty.capitalize())

    array = zip(challenges_user_in, difficulty)

    return shortcuts.render(request,
                            'cccenter/profile.html',
                            {'user':user,
                             'userprofile':userprofile,
                             'challenges_user_in':array,
                             "title":"Code and Cipher Center",
                             "notifications" : notify.get_notifications(request.user, False),
                             "unseen_notification" : notify.unviewed_notifications(request.user)
                            }
                           )

def tutorial(request):
    '''Returns the tutorial page.'''
    return shortcuts.render(request, 'cccenter/tutorials.html',
                            {"title":"Code and Cipher Center",
                             "active":"tutorial"}
                           )

@login_required
def notifications(request):
    '''Returns all notifications for a user.'''
    return shortcuts.render(request, 'cccenter/notifications.html',
                            {"notifications" : notify.get_notifications(request.user, False),
                             "unseen_notification" : notify.unviewed_notifications(request.user),
                             "all_notifications" : notify.get_notifications(request.user, True)})
@login_required
def settings(request):
    '''Try getting the user profile, if it does not exists create one.

       If called with a GET request, returns settings page.

       If called with POST, create settings, user, and password forms.
       Update all the corresponding tables and return the profile page.'''
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if password_form.is_valid():
            password_form.save()
            auth.update_session_auth_hash(request, password_form.user)

        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        if settings_form.is_valid():
            settings_form.save()

        return HttpResponseRedirect('/profile/')

    return shortcuts.render(request, 'cccenter/settings.html',
                            {"title":"Code and Cipher Center",
                             "notifications":notify.get_notifications(request.user, False),
                             "unseen_notification" : notify.unviewed_notifications(request.user)
                            }
                           )

