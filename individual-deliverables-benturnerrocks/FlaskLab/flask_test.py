from app import *
import unittest

class TestSOMETHING(unittest.TestCase):
    def test_route(self):
        self.app = app.test_client()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(b'hello, this is the homepage', response.data)