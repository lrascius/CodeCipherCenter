'''Generates challenge lists'''

import cccenter.models as models
from django.contrib.auth.models import User
from django.utils import timezone

def challenge_list():
    chList = []
    i = Challenge.objects.all()

    for names in i:
        chList.append(names)


