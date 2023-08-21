"""
Django AppConfig for Blogs App
"""
from django.apps import AppConfig


class BlogsConfig(AppConfig):
    """
    Configuration class for the 'blogs' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogs'
