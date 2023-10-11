"""
Celery Tasks for Email Sending and Sleeping
"""
from time import sleep
from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
# pylint: disable=useless-return
def sleepy(duration):
    """
    Celery Task for Simulating Sleeping.
    :param duration: The duration (in seconds) for which the task should sleep.
    :return: None
    """
    sleep(duration)
    return None


@shared_task
# pylint: disable=useless-return
def send_mail_task(user_id):
    """
    Celery Task for Sending Welcome Emails
    :param user_id: The ID of the user to whom the welcome email should be sent.
    :return: None
    """
    user = User.objects.get(pk=user_id)
    name = str(user.first_name).upper() + ' ' + str(user.last_name).upper()
    send_mail('Welcome To Blogy!',
              'WELCOME ' + name +
              '!\n\nThankyou for creating an account with us. '
              'We look forward to working with you.\n\nRegards,\nTeam Blogy',
              'eemaan.amir@gmail.com', ['eemaan.amir@gmail.com'], fail_silently=False)
    return None

# RUN CELERY: python3 -m celery -A djangoproject worker -l info -P eventlet -E
