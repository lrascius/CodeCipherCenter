import unittest2 as unittest
from cccenter.python.general import *

class TestGeneral(unittest.TestCase):
    def test_generateParagraph(self):
        a = generate_paragraph()
        self.assertEqual(type(a), str)
        self.assertGreater(len(a), 0)
