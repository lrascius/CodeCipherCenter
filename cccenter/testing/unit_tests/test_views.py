
import unittest
from unittest.mock import patch
import cccenter.views as views
from django.test import TestCase

class TestViews(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get('/register')
        self.assertEqual(resp.status_code, 200)

    def test_getCipher(self):
        resp = self.client.get('/cccenter/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)

    def test_auth_view(self):
        resp = self.client.get('/accounts/loggedin/')
        self.assertEqual(resp.status_code, 200)

    def test_loggedin(self):
        resp = self.client.get('/accounts/loggedin/')
        self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        resp = self.client.get('/accounts/logout/')
        self.assertEqual(resp.status_code, 200)
