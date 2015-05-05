#!cccenter/python/general.py
'''Grabs text from the Gutenberg Project to use as a plaintext.'''
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from cccenter.models import Notification
import random
import re

# Function that generates a random paragraph from a book.
def generate_paragraph():
    '''Grabs text from the Gutenberg Project.'''
    #Get the text from Gutenberg Project, in this case its Moby Dick
    text = strip_headers(load_etext(2701)).strip()
    #text = "Jack and Jill ran up the hill to get a pail of water. " +
    #       "Jack fell down and broke his crown and Jill came tumbling after."
    sentences = []
    paragraph = ""

    for sentence in text.split("."):
        sentences.append(sentence)

    #Select 2 random sentences
    paragraph = random.choice(sentences) + random.choice(sentences)

    paragraph = re.sub(r'\s+', '', paragraph)
    regex = re.compile('[^a-zA-Z]')
    paragraph = regex.sub('', paragraph).lower()
    return paragraph

def get_notifications(username):
    '''Grabs a users notifications'''
    notifications = Notification.objects.filter(user=username)
    return notifications

def unviewed_notifications(username):
    '''Checks if there is any unviewed notifications for a user'''
    notifications = Notification.objects.filter(user=username, viewed=False)
    if (len(notifications) != 0):
        return True
    else:
        return False

def viewed_notification(username, notification_id):
    '''Sets the notification as viewed when a user clicks on it'''
    notifications = Notification.objects.filter(user=username, viewed=False)

    for notification in notifications:
        if(int(notification.id) == int(notification_id)):
            notification.viewed = True
            notification.save()
            return True

    return False