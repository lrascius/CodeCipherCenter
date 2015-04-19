from django.test import TestCase
from cccenter.python.challenge import *

class TestChallenge(TestCase):
    def test_challengeList(self):
        a = challenge_list()
        self.assertEqual(type(a), str)
        self.assertGreater(len(a), 0)
