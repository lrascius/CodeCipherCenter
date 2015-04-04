#!cccenter/python/cuser.py
'''Extends the Django User class.'''

from django.contrib.auth.models import User

class CUser(User):
    '''Extends the Django user class.'''

    def __init__(self):
        '''Default constructor.'''
        super(CUser, self).__init__()
        #TODO implement class

