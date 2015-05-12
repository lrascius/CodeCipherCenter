from django.test import TestCase
from cccenter.python.general import *
from cccenter.models import *
import mock

class TestGeneral(TestCase):
    def test_generateParagraph(self):
        a = generate_paragraph()
        self.assertEqual(type(a), str)
        self.assertGreater(len(a), 0)
