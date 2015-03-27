#!cccenter/urls.py
'''Contains all urls for the cccenter app.'''

from django.conf.urls import patterns, url
from cccenter import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^getcipher/$', views.getCipher, name="getCipher"),
                      )
