
import unittest
from unittest.mock import patch
from cccenter.views import *
from django.test import TestCase
from django.test.client import Client

class TestViews(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        ''' Test registration form (get and post requests)'''
        
        # test if registration form is returned to get request
        resp = self.client.get('/register')
        self.assertEqual(resp.status_code, 200)
        
        # empty post request to test response to incorrect post
        resp = self.client.post('/register')
        self.assertEqual(resp.status_code, 200)
        
        # test correct response
        resp = self.client.post('/register', {'username':'mk', 'first_name':'m', 'last_name':'k', 'email':'mk@example.com', 
                                              'password1':'a', 'password2':'a'})
        self.assertEqual(resp.status_code, 200)

    def test_getCipher(self):
        resp = self.client.get('/getcipher/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        response = self.client.get('/accounts/login/')

       	
       	value = client.login(username='fred', password='secret')
       	self.assertEqual(value, False)
       	value = client.logout()
       	self.assertEqual(value, None)

    def test_auth_view(self):
        ''' Test authorization '''
        
        # test bad authorization
        resp = self.client.post('/accounts/auth/', {'username':'t1', 'password':'1'})
        self.assertEqual(resp.status_code, 200)

        # test good authorization
        resp = self.client.post('/accounts/auth/', {'username':'marctest0', 'password':'marc'})
        self.assertEqual(resp.status_code, 200)

    def test_loggedin(self):
        response = self.client.get('/accounts/loggedin/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
