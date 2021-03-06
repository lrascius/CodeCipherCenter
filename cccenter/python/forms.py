#!forms.py
'''Holds the forms used in the website.'''

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from cccenter.models import UserProfile

class RegistrationForm(UserCreationForm):
    '''A form for creating a new user

    Meta class for registration form is provided. It connects the form to the User model and gives \
    proper fields for the form.

    Fields used in the form:

    :field username: Username of the new user
    :field first_name: (optional) First name of the new user
    :field last_name: (optional) Last name of the new user
    :field email: Email of the new user
    :field password1: Password of the new user (must match password2)
    :field password2: Password of the new user (must match password1)
    '''

    email = forms.EmailField(required=True)

    class Meta:
        '''Provides the fields for the registration form.'''
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SettingsForm(forms.ModelForm):
    '''User account settings form

    Meta class for user settings form is provided. It connects the form to the user settings page\
    and provides the proper fields for the form.

    Fields used in the form:

    :field profile_image: Profile image of the user (default is provided)
    '''

    # :description model: Model is the UserProfile model where user information is stored
    # :description fields: Fields are the fields used in the form'''

    class Meta:
        '''Provides the fields for the settings form.'''
        model = UserProfile
        fields = ('profile_image',)

