import json
import unittest

from application.app import create_app
from application.config import TestConfig


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
#        db.create_all()
        self.client = self.app.test_client()
        self.api_url = 'api/v1/version'
        self.fake_url = 'api/v1/fake_ur;'

    def tearDown(self):
#        db.session.remove()
#        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get(self.fake_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_200(self):
        response = self.client.get(
            self.api_url,
        )
        self.assertEqual(response.status_code, 200)

