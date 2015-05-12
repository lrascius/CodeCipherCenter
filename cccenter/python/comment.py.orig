#!cccenter/python/comment.py
'''
Interfaces with the Comment model.
'''

from cccenter import models

def get_comments(challenge_id):
    '''
    Returns the comments associated with the given Challenge.
    
    :param challenge_id: The challenge's associated object's id number
    :type challenge_id: int
    :return: All the comments associated with the challenge
    :rtype: [models.Comment]
    
    .. note:: The return type is actually a query set, but can be treated as a list of Comment objects.
    '''
    if isinstance(challenge_id, int) == False:
        raise TypeError("challenge_id is " + str(type(challenge_id)) + ", not int")

    challenge = models.Challenge.objects.get(pk=challenge_id)

    if challenge == None:
        raise ValueError("Invalid challenge_id")

    comments = challenge.challenge_comment_set.all()

    return comments
