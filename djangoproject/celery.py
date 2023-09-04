"""
Celery Configuration Module for Django Project
"""
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('djangoproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    A Celery task for debugging purposes.

    This task is used for debugging and can be called with any arbitrary arguments.
    It simply prints the request object for debugging purposes.

    :param self: The task instance.
    """
    print(f'Request: {self.request!r}')
