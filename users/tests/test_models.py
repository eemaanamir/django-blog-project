from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileModelTest(TestCase):

    def test_create_user_profile(self):
        self.assertEqual(Profile.objects.count(), 0)

        user = User.objects.create(username='123@123.com')
        user.save()
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_save_user_profile(self):
        user = User.objects.create(username='testuser')
        user.save()

        user.username = 'updated'
        user.save()

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, 'updated')
