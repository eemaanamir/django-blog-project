"""
User Forms Tests Module
This module contains test cases for the user-related forms.
"""
from django.test import TestCase
from users.forms import UserSignupForm, ProfileSignupForm, UserEditForm, ProfileEditForm


class TestUserSignupForm(TestCase):
    """
    Test cases for the UserSignupForm.
    """

    def test_correct_input(self):
        """
        Test form validation with correct input data.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': 'eemaan@gmail.com',
            'password1': 'One23456789',
            'password2': 'One23456789',
        }
        form = UserSignupForm(data)
        self.assertTrue(form.is_valid())

    def test_incorrect_email_format(self):
        """
        Test form validation when email is already taken.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': 'eemaan.com',
            'password1': 'One23456789',
            'password2': 'One23456789',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ["Enter a valid email address."])

    def test_email_already_taken(self):
        """
        Test form validation when email is already taken.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': '123@123.com',
            'password1': 'One23456789',
            'password2': 'One23456789',
        }
        form1 = UserSignupForm(data)
        form1.save()
        form2 = UserSignupForm(data)
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors['email'],
                          ["This email is already in use. Please use a different email."])

    def test_passwords_not_matching(self):
        """
        Test form validation when passwords do not match.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': 'eemaan@gmail.com',
            'password1': 'One23456789',
            'password2': 'One23456',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])

    def test_field_length_limit_exceeded(self):
        """
        Test form validation when field length limit is exceeded.
        """
        data = {
            'first_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'last_name': 'Amir',
            'email': 'eemaan@gmail.com',
            'password1': 'One23456789',
            'password2': 'One23456',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'],
                          ["Ensure this value has at most 150 characters (it has 204)."])

    def test_missing_fields(self):
        """
        Test form validation when required fields are missing.
        """
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])


class TestProfileSignupForm(TestCase):
    """
    Test cases for the ProfileSignupForm.
    """

    def test_correct_input(self):
        """
        Test form validation with correct input data.
        """
        data = {
            'user_bio': 'Hello World! I am Eemaan.',
        }
        form = ProfileSignupForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        """
        Test form validation when field length limit is exceeded.
        """
        data = {
            'user_bio': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
        }
        form = ProfileSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['user_bio'],
                          ['Ensure this value has at most 200 characters (it has 204).'])

    def test_missing_fields(self):
        """
        Test form validation when required fields are missing.
        """
        data = {
            'user_bio': '',
        }
        form = ProfileSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['user_bio'], ['This field is required.'])


class TestUserEditForm(TestCase):
    """
    Test cases for the UserEditForm.
    """

    def test_correct_input(self):
        """
        Test form validation with correct input data.
        """
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
        }
        form = UserEditForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        """
        Test form validation when field length limit is exceeded.
        """
        data = {
            'first_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'last_name': 'Amir',
        }
        form = UserEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'],
                          ["Ensure this value has at most 150 characters (it has 204)."])

    def test_missing_fields(self):
        """
        Test form validation when required fields are missing.
        """
        data = {
            'first_name': '',
            'last_name': '',
        }
        form = UserEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])


class TestProfileEditForm(TestCase):
    """
    Test cases for the ProfileEditForm.
    """

    def test_correct_input(self):
        """
        Test form validation with correct input data.
        """
        data = {
            'user_bio': 'Hello World! I am Eemaan.',
        }
        form = ProfileEditForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        """
        Test form validation when field length limit is exceeded.
        """
        data = {
            'user_bio': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
        }
        form = ProfileEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['user_bio'],
                          ['Ensure this value has at most 200 characters (it has 204).'])

    def test_missing_fields(self):
        """
        Test form validation when required fields are missing.
        """
        data = {
            'user_bio': '',
        }
        form = ProfileEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['user_bio'], ['This field is required.'])
