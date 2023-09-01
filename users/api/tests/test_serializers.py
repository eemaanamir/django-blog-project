"""
Module: users.api.tests.test_serializers
Description: This module contains test cases for the Users API app.
"""
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from users.models import User, Profile
from users.api.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    ProfileDetailUpdateSerializer,
    UserDetailUpdateSerializer
)


class UserCreateSerializerTest(TestCase):
    """
    Test cases for the UserCreateSerializer class.
    """
    def test_valid_user_create_serializer(self):
        """Test valid user creation serializer."""
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': '123@123.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_bio': 'Hello, I am Eemaan.'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_email_already_in_use(self):
        """Test email already in use validation."""
        User.objects.create_user(username='123@123.com',
                                 email='123@123.com', password='testpassword')
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': '123@123.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_bio': 'Hello, I am Eemaan.'
        }
        serializer = UserCreateSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['email'][0],
                         'This email is already in use. Please use a different email.')

    def test_invalid_user_create_serializer(self):
        """Test invalid user creation serializer."""
        data = {
            'first_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'last_name': 'Amir',
            'email': '123.com',
            'password1': 'testpassword',
            'password2': 'password',
            'user_bio': ''
        }
        serializer = UserCreateSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['first_name'][0],
                         'Ensure this value has at most 150 characters (it has 204).')
        self.assertEqual(context.exception.detail['email'][0], 'Enter a valid email address.')
        self.assertEqual(context.exception.detail['password2'][0], 'Passwords must match.')
        self.assertEqual(context.exception.detail['user_bio'][0], 'This field may not be blank.')


class UserLoginSerializerTest(TestCase):
    """
    Test cases for the UserLoginSerializer class.
    """
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')

    def test_valid_user_login_serializer(self):
        """Test valid user login serializer."""
        data = {
            'email': '123@123.com',
            'password': 'testpassword'
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_user_login_serializer(self):
        """Test invalid user login serializer."""
        data = {
            'email': '123@123.com',
            'password': 'wrongpassword'
        }
        serializer = UserLoginSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail['non_field_errors'][0],
                         'Incorrect credentials please try again.')


class ProfileDetailUpdateSerializerTest(TestCase):
    """
    Test cases for the ProfileDetailUpdateSerializer class.
    """
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.profile = Profile.objects.get(user_id=self.user)

    def test_valid_profile_update_serializer(self):
        """Test valid profile update serializer."""
        data = {
            'user_bio': 'Updated bio'
        }
        serializer = ProfileDetailUpdateSerializer(instance=self.profile, data=data)
        self.assertTrue(serializer.is_valid())

    def test_length_limit_exceeded_profile_update_serializer(self):
        """Test profile update serializer with length limit exceeded."""
        data = {
            'user_bio': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
        }
        serializer = ProfileDetailUpdateSerializer(instance=self.profile, data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail['user_bio'][0],
                         'Ensure this value has at most 200 characters (it has 204).')

    def test_missing_field_profile_update_serializer(self):
        """Test profile update serializer with missing field."""
        data = {
            'user_bio': ''
        }
        serializer = ProfileDetailUpdateSerializer(instance=self.profile, data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail['user_bio'][0], 'This field may not be blank.')


class UserDetailUpdateSerializerTest(TestCase):
    """
    Test cases for the UserDetailUpdateSerializer class.
    """
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')
        self.profile = Profile.objects.get(user_id=self.user)

    def test_valid_user_detail_update_serializer(self):
        """Test valid user detail update serializer."""
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'profile': {
                'user_bio': 'Updated bio'
            }
        }
        serializer = UserDetailUpdateSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())

    def test_length_limit_exceeded_profile_update_serializer(self):
        """Test user detail update serializer with length limit exceeded."""
        data = {
            'first_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'last_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                         'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                         'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                         'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'profile': {
                'user_bio': 'Updated bio'
            }
        }
        serializer = UserDetailUpdateSerializer(instance=self.user, data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['first_name'][0],
                         'Ensure this value has at most 150 characters (it has 204).')
        self.assertEqual(context.exception.detail['last_name'][0],
                         'Ensure this value has at most 150 characters (it has 204).')

    def test_missing_user_detail_update_serializer(self):
        """Test user detail update serializer with missing field."""
        data = {
            'first_name': '',
            'last_name': '',
            'profile': {
                'user_bio': 'Updated bio'
            }
        }
        serializer = UserDetailUpdateSerializer(instance=self.user, data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual(context.exception.detail['first_name'][0], 'This field may not be blank.')
        self.assertEqual(context.exception.detail['last_name'][0], 'This field may not be blank.')
