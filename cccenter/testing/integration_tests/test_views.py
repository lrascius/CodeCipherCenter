from unittest.mock import patch
import cccenter.views as views
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
import json

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="m", password="t")
        self.client.login(username="m", password="t")
        
    def tearDown(self):
        self.user.delete()

    #@patch.mock('cccenter.views.django.shortcuts.render')
    #@patch.mock('cccenter.views.request')
    #def test_index(self, mock_request, mock_render):
    #    #response = self.client.get('/')
    #    views.index(mock_request)
        
        #self.assertEqual(response.status_code, 200)
    #    mock_render.assert_called_with(mock_request, 'cccenter/challenge_page.html', {"title":"Code and Cipher Center"})

    def test_register(self):
        ''' Test registration form (get and post requests)'''
        # test if registration form is returned to get request
        resp = self.client.get('/accounts/register/')
        self.assertEqual(resp.status_code, 200)
        
        # empty post request to test response to incorrect post
        resp = self.client.post('/accounts/register/')
        self.assertEqual(resp.status_code, 200)
        
        # test correct response
        resp = self.client.post('/accounts/register/', {'username':'mk', 'first_name':'m', 'last_name':'k', 'email':'mk@example.com', 
                                              'password1':'a', 'password2':'a'})
        self.assertEqual(resp.status_code, 200)

    def test_getCipher(self):
        resp = self.client.get('/getcipher/')
        self.assertEqual(resp.status_code, 200)

    def test_challengeList(self):
        resp = self.client.get('/cipher/challengelist/')
        self.assertEqual(resp.status_code, 200)
        
    def test_challengeCreation(self):
        #response = self.client.get('/cipher/createchallenge/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')

        resp = self.client.post('/cipher/createchallenge/')
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content.decode('utf-8'))
        self.assertTrue(data['ciphertext'])
        self.assertTrue(data['challenge_id'])
        
        resp = self.client.get('/cipher/createchallenge/')
        self.assertEqual(resp.status_code, 200)
        
    def test_challengePage(self):
        resp = self.client.get('/cipher/challengepage/', {'challenge_id':'20'})
        self.assertNotEqual(resp, None)
        self.assertEqual(resp.status_code, 200)
        
    def test_joinChallenge(self):
        resp = self.client.post('/cipher/joinchallenge/', {'challenge_id':'20'})
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.get('/cipher/joinchallenge/', {'challenge_id':'20'})
        self.assertEqual(resp.status_code, 404)
        
    def test_checkPlaintext(self):
        response = self.client.get('/cipher/checkplaintext/', follow=True)
        self.assertRedirects(response, '/accounts/login/')

        resp = self.client.post('/cipher/checkplaintext/', {'challenge_id':'1', 'user_id':2, 'guessed_plaintext':'def'})
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(type(data), bool)

    def test_login(self):
        response = self.client.get('/accounts/login/')

        value = self.client.login(username='fred', password='secret')
        self.assertEqual(value, False)
        value = self.client.logout()
        self.assertEqual(value, None)

    def test_auth_view(self):
        ''' Test authorization '''
        
        # test bad authorization
        resp = self.client.post('/accounts/auth/', {'username':'t1', 'password':'1'})
        self.assertEqual(resp.status_code, 200)

        # test good authorization
        resp = self.client.post('/accounts/auth/', {'username':'marctest0', 'password':'test0'})
        self.assertEqual(resp.status_code, 200)

    def test_loggedin(self):
        response = self.client.get('/accounts/loggedin/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        #response = self.client.get('/accounts/logout', follow=True)
        #self.assertRedirects(response, '/accounts/login/')        
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        #response = self.client.get('/profile/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cccenter/profile.html')

    def test_settings(self):
        #response = self.client.get('/settings/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)
        #response = self.client.post('/settings', {})
        #self.assertTemplateUsed(response, 'cccenter/settings.html')

