# from unittest.mock import patch
import cccenter.views as views
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.utils import timezone
from cccenter.models import *
import json

class TestViews(TestCase):
    def setUp(self):
        self.tn = timezone.now()
        self.user = User.objects.create_superuser(username="m", password="t", email="mt@example.com")
        self.client.login(username="m", password="t")
        self.cipher = Cipher.objects.create(ciphertype='Caesar Shift Cipher', difficulty='advanced')
        self.challenge = Challenge.objects.create(plaintext='plaintext', ciphertext='ciphertext', ciphertype='Caesar Shift Cipher',
                                                  cipherkey='key', challenge_type='single', datetime_created=self.tn)
        self.challenge.cipher.add(self.cipher)
        self.challenge.users.add(self.user)
        self.challenge.solved = True
        self.challenge.solved_by.add(self.user)
        self.challenge.save()
        self.challenge_id = self.challenge.id
        
    def tearDown(self):
        self.client.logout()
        self.challenge.delete()
        self.user.delete()
        self.cipher.delete()

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

        with open('cccenter/testing/html_validation/register1.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    # def test_register_2(self):
    #     # empty post request to test response to incorrect post
    #     resp = self.client.post('/accounts/register/')
    #     self.assertEqual(resp.status_code, 404)
        
        #with open('cccenter/testing/html_validation/register2.html', 'w') as outfile:
        #    outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    def test_register_3(self):
        # test correct response
        resp = self.client.post('/accounts/register/', {'username':'mk', 'first_name':'m', 'last_name':'k', 'email':'mk@example.com', 
                                              'password1':'a', 'password2':'a'})
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/register3.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_getCipher(self):
        resp = self.client.get('/getcipher/')
        self.assertEqual(resp.status_code, 200)

    def test_challengeList(self):
        resp = self.client.get('/cipher/challengelist/')
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/challengelist1.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    def test_challengeCreation(self):
        #response = self.client.get('/cipher/createchallenge/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')

        resp = self.client.post('/cipher/createchallenge/')
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/createchallenge1.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
        #data = json.loads(resp.content.decode('utf-8'))
        #self.assertTrue(data['ciphertext'])
        #self.assertTrue(data['challenge_id'])
        
        resp = self.client.get('/cipher/createchallenge/')
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/createchallenge2.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    def test_challengePage(self):
        resp = self.client.get('/cipher/challengepage/', {'challenge_id':int(self.challenge_id)})
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/challengepage1.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    def test_joinChallenge(self):
        resp = self.client.post('/cipher/joinchallenge/', {'challenge_id':int(self.challenge_id)})
        self.assertEqual(resp.status_code, 302)
        
        #with open('cccenter/testing/html_validation/joinchallenge1.html', 'w') as outfile:
        #    outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))
        
    # def test_joinChallenge_2(self):
    #     resp = self.client.get('/cipher/joinchallenge/', {'challenge_id':'1'})
    #     self.assertEqual(resp.status_code, 302)
        
    def test_checkPlaintext(self):
        #response = self.client.get('/cipher/checkplaintext/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')

        resp = self.client.post('/cipher/checkplaintext/', {'challenge_id':int(self.challenge_id), 'user_id':2, 'guessed_plaintext':'a'})
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(type(data), dict)
        self.assertFalse(data['success'])
        
    def test_checkPlaintext_2(self):
        #response = self.client.get('/cipher/checkplaintext/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')

        resp = self.client.post('/cipher/checkplaintext/', {'challenge_id':int(self.challenge_id), 'user_id':2,
                                                            'guessed_plaintext':self.challenge.plaintext})
        self.assertEqual(resp.status_code, 200)
        
        data = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(type(data), dict)
        self.assertTrue(data['success'])

    def test_login(self):
        response = self.client.get('/accounts/login/')

        value = self.client.login(username='fred', password='secret')
        self.assertEqual(value, False)
        value = self.client.logout()
        self.assertEqual(value, None)
        
        with open('cccenter/testing/html_validation/login1.html', 'w') as outfile:
            outfile.write(str(response.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_auth_view(self):
        ''' Test authorization '''
        
        # test bad authorization
        resp = self.client.post('/accounts/auth/', {'username':'t1', 'password':'1'})
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/auth1.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

        # test good authorization
        resp = self.client.post('/accounts/auth/', {'username':'marctest0', 'password':'test0'})
        self.assertEqual(resp.status_code, 200)
        
        with open('cccenter/testing/html_validation/auth2.html', 'w') as outfile:
            outfile.write(str(resp.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_loggedin(self):
        response = self.client.get('/accounts/loggedin/')
        #self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        
        #with open('cccenter/testing/html_validation/loggedin1.html', 'w') as outfile:
        #    outfile.write(str(response.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_logout(self):
        #response = self.client.get('/accounts/logout', follow=True)
        #self.assertRedirects(response, '/accounts/login/')        
        response = self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')
        
        #with open('cccenter/testing/html_validation/logout1.html', 'w') as outfile:
        #    outfile.write(str(response.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_profile(self):
        #response = self.client.get('/profile/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cccenter/profile.html')
        
        with open('cccenter/testing/html_validation/profile1.html', 'w') as outfile:
            outfile.write(str(response.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

    def test_settings(self):
        #response = self.client.get('/settings/', follow=True)
        #self.assertRedirects(response, '/accounts/login/')
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)
        #response = self.client.post('/settings', {})
        #self.assertTemplateUsed(response, 'cccenter/settings.html')
        
        with open('cccenter/testing/html_validation/settings1.html', 'w') as outfile:
            outfile.write(str(response.content)[2:-1].replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'"))

if __name__ == "__main__":
    unittest.run()
