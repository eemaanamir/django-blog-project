from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
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
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
