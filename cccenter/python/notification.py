#!cccenter/python/notification.py
'''Contains functions primarily focused on the notification model.'''

from cccenter.models import Notification, Challenge
from django.utils import timezone
from django.contrib.auth.models import User

def get_notifications(user, get_all=False):
    '''
    Gets notifications

    :param user: current user
    :param get_all: If set to true will get all the notifications, if set to false returns \
    5 most recent notifications
    :type user: models.User
    :type get_all: boolean
    :return: All the user's notifications or the 5 most recent
    :rtype: [models.User]

    .. note:: The return type is actually a query set, but can be treated as a list of User objects.
    '''
    if get_all == True:
        notifications = Notification.objects.filter(user=user).order_by('-datetime')
    else:
        notifications = Notification.objects.filter(user=user).order_by('-datetime')[:5]
    return notifications

def unviewed_notifications(user):
    '''
    Checks if there is any unviewed notifications for a user

    :param user: Current user
    :type user: models.User
    :return: True if there is more than one unviewed notification, else False \
    meaning that the user has no unviewed notifications
    :rtype: boolean
    '''
    notifications = Notification.objects.filter(user=user, viewed=False)
    if len(notifications) != 0:
        return True
    else:
        return False

def viewed_notification(user, notification_id):
    '''
    Sets a notification to viewed based on the user and notification_id

    :param user: Current user
    :type user: models.User
    :param notification_id: id of the notification object
    :type notification_id: int
    :return: Was the notification viewed parameter succesfully set to true
    :rtype: boolean
    '''
    notifications = Notification.objects.filter(user=user, viewed=False)

    for notification in notifications:
        if int(notification.id) == int(notification_id):
            notification.viewed = True
            notification.save()
            return True

    return False

def solved_cipher_notification(username, challenge_id):
    '''
    Notifies the users when a challenge has been solved for the first time, all users \
    of that challenge will receive a notification telling them the user who has solved \
    the challenge and a link to that page

    :param user: username
    :type user: string
    :param challenge_id: id of the challenge 
    :type challenge_id: int
    '''

    solved_by = Challenge.objects.filter(pk=int(challenge_id))[0].solved_by.all()

    if(len (solved_by) == 1):
        users_in_challenge = Challenge.objects.filter(pk=int(challenge_id))[0].users.all()
        for user in users_in_challenge:
            if(user.username == str(username)):
                continue

            link = "/cipher/challengepage/?challenge_id=" + str(challenge_id)
            notify_message = str(username) + " has solved challenge # "\
                             + str(challenge_id)

            notification = Notification(user=user, notification=notify_message,
                                        link=link, datetime=timezone.now())
            notification.save()
