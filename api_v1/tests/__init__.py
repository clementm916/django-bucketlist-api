from django.test import modify_settings
from rest_framework.test import APITestCase


import django
django.setup()

from django.contrib.auth.models import User


@modify_settings(
    ALLOWED_HOSTS={'append': 'testserver'}
)
class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.test_client = self.client
        self.user = User(username='clemn', password='password123')
        self.user.save()

        request = self.test_client.post(
            '/api/v1/auth/login', {'username': 'clemn', 'password': 'password123'})
        token = request.data['token']

        self.auth = token
