from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import modify_settings


@modify_settings(
    ALLOWED_HOSTS={'append': 'testserver'}
)
class Test_User_Authentication(APITestCase):
    def setUp(self):
        self.test_client = self.client

    def test_user_registration(self):
        payload = {'username': 'clemn', 'password': 'password123'}
        request = self.test_client.post(
            '/api/v1/auth/register', payload, format='json')
        self.assertEqual(request.status_code, 201)
        self.assertIn('clemn', str(request.data))

    def test_user_login(self):
        user = User(username='clemn', password='password123')
        user.save()
        payload = {'username': 'clemn', 'password': 'password123'}
        request = self.test_client.post(
            '/api/v1/auth/login', payload, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertIn('token', str(request.data))

        # with wrong password
        user = User(username='clemn', password='password123')
        user.save()
        payload = {'username': 'clemn', 'password': 'wrongpass'}
        request = self.test_client.post(
            '/api/v1/auth/login', payload, format='json')
        self.assertEqual(request.status_code, 400)

    def test_accessing_endpoint_with_authentication(self):
        user = User(username='clemn', password='password123')
        user.save()
        payload = {'username': 'clemn', 'password': 'password123'}
        request = self.test_client.post(
            '/api/v1/auth/login', payload, format='json')
        self.assertEqual(request.status_code, 200)
        auth = {'Authorization': request.data['token']}
        request = self.test_client.get(
            '/api/v1/bucketlists/', HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(request.status_code, 200)

    def test_accessing_endpoint_without_authentication(self):
        request = self.test_client.get(
            '/api/v1/bucketlists/', format='json')
        self.assertEqual(request.status_code, 400)
