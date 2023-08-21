"""
User Views Tests Module
This module contains test cases for the user-related views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile


class TestLoginView(TestCase):
    """
    Test cases for the login view.
    """
    def setUp(self):
        """
        Set up the client and create a user for testing.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword')

    def tearDown(self):
        """
        Clean up by deleting the test user.
        """
        self.user.delete()

    def test_valid_credentials(self):
        """
        Test logging in with valid credentials.
        """
        response = self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_invalid_credentials(self):
        """
        Test logging in with invalid credentials.
        """
        response = self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error while logging in: Invalid Credentials!',
                      response.context['login_form_errors'])


class TestSignupView(TestCase):
    """
    Test cases for the signup view.
    """
    def setUp(self):
        """
        Set up the client.
        """
        self.client = Client()

    def test_correct_input(self):
        """
         Test signing up with correct input data.
         """
        response = self.client.post(reverse('signup'), {
            'f_name': 'Eemaan',
            'l_name': 'Amir',
            'new_email': 'eemaan@gmail.com',
            'pass1': 'One23456789',
            'pass2': 'One23456789',
            'bio': 'Hello World! I am Eemaan.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_incorrect_input(self):
        """
        Test signing up with incorrect input data.
        """
        response = self.client.post(reverse('signup'), {
            'f_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                      'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                      'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                      'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'l_name': '',
            'new_email': 'eemaan.gmail.com',
            'pass1': 'One23456789',
            'pass2': 'One234567',
            'bio': 'Hello World! I am Eemaan.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ensure this value has at most 150 characters (it has 204).',
                      response.context['signup_form_errors']['first_name'])
        self.assertIn('This field is required.',
                      response.context['signup_form_errors']['last_name'])
        self.assertIn('Enter a valid email address.',
                      response.context['signup_form_errors']['email'])
        self.assertIn('The two password fields didn’t match.',
                      response.context['signup_form_errors']['password2'])


class TestEditProfileView(TestCase):
    """
    Test cases for the edit profile view.
    """
    def setUp(self):
        """
        Set up the client, create a user, and log in.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword',
                                             first_name='Eemaan', last_name='Amir')
        self.profile = Profile.objects.get(user_id=self.user)
        self.profile.user_bio = 'Hello World! I am Eemaan.'
        self.client.login(username='123@123.com', password='testpassword')

    def tearDown(self):
        """
        Clean up by deleting the test user and profile.
        """
        self.profile.delete()
        self.user.delete()

    def test_correct_input(self):
        """
        Test editing profile with correct input data.
        """
        response = self.client.post(reverse('edit_profile'), {
            'input-first-name': 'Eemaan2',
            'input-last-name': 'Amir2',
            'user-bio-input': 'Hello World! Updated Bio.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_profile'))

        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Eemaan2')
        self.assertEqual(self.user.last_name, 'Amir2')
        self.assertEqual(self.profile.user_bio, 'Hello World! Updated Bio.')

    def test_incorrect_input(self):
        """
        Test editing profile with incorrect input data.
        """
        response = self.client.post(reverse('edit_profile'), {
            'input-first-name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                                'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                                'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                                'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'input-last-name': '',
            'user-bio-input': 'Hello World! Updated Bio.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ensure this value has at most 150 characters (it has 204).',
                      response.context['form_errors']['first_name'])
        self.assertIn('This field is required.',
                      response.context['form_errors']['last_name'])


class TestEditDPView(TestCase):
    """
    Test cases for the edit profile picture view.
    """
    def setUp(self):
        """
        Set up the client, create a user, and log in.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='123@123.com',
                                             email='123@123.com', password='testpassword',
                                             first_name='Eemaan', last_name='Amir')
        self.profile = Profile.objects.get(user_id=self.user)
        self.profile.user_bio = 'Hello World! I am Eemaan.'
        self.client.login(username='123@123.com', password='testpassword')

    def tearDown(self):
        """
        Clean up by deleting the test user and profile.
        """
        self.profile.delete()
        self.user.delete()

    def test_upload_dp(self):
        """
        Test uploading a profile picture.
        """
        with open('./users/tests/test_dp.jpeg', 'rb') as image_file:
            response = self.client.post(reverse('edit_dp'), {'user_dp': image_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.user_dp, 'user_dps/test_dp.jpeg')

    def test_no_file_selected(self):
        """
        Test when no file is selected for upload.
        """
        response = self.client.post(reverse('edit_dp'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('No File Was Selected!', response.context['messages'])
