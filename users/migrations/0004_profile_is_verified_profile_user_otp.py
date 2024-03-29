# Generated by Django 4.2.3 on 2023-10-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_followers_count_remove_profile_followers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
