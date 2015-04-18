from django.test import TestCase
from cccenter.python.general import *

class TestChallenge(TestCase):
    def test_challengeList():
	a = challenge_list()
	self.assertEqual(type(a), str)
	self.assertGreater(len(a), 0)
