"""
User Model Module
This module contains the model definitions and associated signals.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


class Profile(models.Model):
    """
    User profile model containing additional information about the user.
    """
    USER_TYPE_CHOICES = (
        ('basic', 'Basic User'),
        ('premium', 'Premium User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_bio = models.CharField(max_length=200)
    has_credit_card = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='basic')
    user_dp = models.ImageField(upload_to='user_dps/', default='user_dps/default_user_dp.png')
    blog_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, related_name='following')
    is_verified = models.BooleanField(default=False)
    user_otp = models.CharField(max_length=6, null=True, blank=True)

    # pylint: disable=no-member
    def __str__(self):
        return self.user.username

    # pylint: disable=no-self-argument
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):   # pylint: disable=unused-argument
        """
        Signal handler to create a user profile when a new user is created.
        """
        if created:
            Profile.objects.create(user=instance)

    # pylint: disable=no-self-argument
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):  # pylint: disable=unused-argument
        """
        Signal handler to save the user profile when the user is saved.
        """
        instance.profile.save()


# pylint: disable=no-self-argument
@receiver(m2m_changed, sender=Profile.followers.through)
def update_followers_count(sender, instance, action, reverse, model, pk_set, **kwargs): # pylint: disable=unused-argument
    if action == "post_add":
        instance.followers_count = instance.followers.count()
        instance.save()
    elif action == "post_remove":
        instance.followers_count = instance.followers.count()
        instance.save()
