"""
Module: users.api.tests.test_views
Description: This module contains test cases for the Users API app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserCreateAPIViewTest(TestCase):
    """
    Test class for user registration functionality.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.url = reverse('users-api:signup')

    def test_user_create(self):
        """
        Test user creation with valid data.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': '123@123.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_bio': 'Hello World! I am Eemaan.'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, '123@123.com')

    def test_user_create_with_incorrect_data(self):
        """
        Test user creation with valid data.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': '123@123.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_bio': ''
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserLoginAPIViewTest(TestCase):
    """
    Test class for user login functionality.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.url = reverse('users-api:login')
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')

    def test_user_login(self):
        """
        Test user login with valid credentials.
        """
        data = {
            'email': '123@123.com',
            'password': 'testpassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_with_incorrect_credentials(self):
        """
        Test user login with incorrect credentials.
        """
        data = {
            'email': '123@123.com',
            'password': 'incorrectpassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class UserDetailAPIViewTest(TestCase):
    """
    Test class for retrieving user details functionality.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.url = reverse('users-api:profile', args=[self.user.id])

    def get_jwt_token(self):
        """
        Helper function to get JWT token.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_retrieve_user_detail_with_jwt(self):
        """
        Test retrieving user details with JWT.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], '123@123.com')

    def test_retrieve_user_detail_without_jwt(self):
        """
        Test retrieving user details without JWT.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailUpdateAPIViewTest(TestCase):
    """
    Test class for updating user details functionality.
    """
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.url = reverse('users-api:edit_profile', args=[self.user.id])

    def get_jwt_token(self):
        """
        Helper function to get JWT token.
        """
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_update_user_detail_with_jwt(self):
        """
        Test updating user details with JWT.
        """
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'profile': {
                'user_bio': 'Updated user bio'
            }
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['user_bio'], 'Updated user bio')

    def test_update_user_detail_without_jwt(self):
        """
        Test updating user details without JWT.
        """
        data = {
            'profile': {
                'user_bio': 'Updated user bio'
            }
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
