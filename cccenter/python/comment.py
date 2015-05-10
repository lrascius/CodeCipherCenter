#!cccenter/python/comment.py
'''Interface with the Comment model. Returns information about comments
   and their related Challenges and Users.'''

from cccenter import models

def get_comments(challenge_id):
    '''Returns the comments associated with the given Challenge.'''
    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")

    comments = challenge.challenge_comment_set.all()

    return comments
