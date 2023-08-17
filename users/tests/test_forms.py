from django.test import TestCase
from users.forms import UserSignupForm, ProfileSignupForm, UserEditForm, ProfileEditForm


class TestUserSignupForm(TestCase):

    def test_correct_input(self):
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
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': 'eemaan.com',
            'password1': 'One23456789',
            'password2': 'One23456789',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ["Enter a valid email address."])

    def test_email_already_taken(self):
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
        self.assertEquals(form2.errors['email'], ["This email is already in use. Please use a different email."])

    def test_passwords_not_matching(self):
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
            'email': 'eemaan@gmail.com',
            'password1': 'One23456789',
            'password2': 'One23456',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'], ["The two password fields didn’t match."])

    def test_field_length_limit_exceeded(self):
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
        self.assertEquals(form.errors['first_name'], ["Ensure this value has at most 150 characters (it has 204)."])

    def test_missing_fields(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'], ['This field is required.'])
        self.assertEquals(form.errors['last_name'], ['This field is required.'])
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['password1'], ['This field is required.'])
        self.assertEquals(form.errors['password2'], ['This field is required.'])


class TestProfileSignupForm(TestCase):

    def test_correct_input(self):
        data = {
            'user_bio': 'Hello World! I am Eemaan.',
        }
        form = ProfileSignupForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        data = {
            'user_bio': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
        }
        form = ProfileSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['user_bio'], ['Ensure this value has at most 200 characters (it has 204).'])

    def test_missing_fields(self):
        data = {
            'user_bio': '',
        }
        form = ProfileSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['user_bio'], ['This field is required.'])


class TestUserEditForm(TestCase):

    def test_correct_input(self):
        data = {
            'first_name': 'Eemaan',
            'last_name': 'Amir',
        }
        form = UserEditForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        data = {
            'first_name': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                          'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
            'last_name': 'Amir',
        }
        form = UserEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'], ["Ensure this value has at most 150 characters (it has 204)."])

    def test_missing_fields(self):
        data = {
            'first_name': '',
            'last_name': '',
        }
        form = UserEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'], ['This field is required.'])
        self.assertEquals(form.errors['last_name'], ['This field is required.'])


class TestProfileEditForm(TestCase):

    def test_correct_input(self):
        data = {
            'user_bio': 'Hello World! I am Eemaan.',
        }
        form = ProfileEditForm(data)
        self.assertTrue(form.is_valid())

    def test_field_length_limit_exceeded(self):
        data = {
            'user_bio': 'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan'
                        'EemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaanEemaan',
        }
        form = ProfileEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['user_bio'], ['Ensure this value has at most 200 characters (it has 204).'])

    def test_missing_fields(self):
        data = {
            'user_bio': '',
        }
        form = ProfileEditForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['user_bio'], ['This field is required.'])






























