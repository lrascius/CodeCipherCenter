#!forms.py
'''Holds the forms used in the website.'''

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    '''User registration form.'''

    email = forms.EmailField(required=True)

    class Meta:
        '''Meta class for registration form. Connects form to the User model and gives
           proper fields for the form.'''
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

