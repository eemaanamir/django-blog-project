"""
Django Admin Configuration for Models

This module contains the Django admin configuration for various models in the project.
It registers the models with the admin site, allowing them to be managed and edited
through the Django admin interface.
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
