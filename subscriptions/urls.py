"""
Module: blog_api.urls
Description: This module defines the URL patterns for the Blog API app.

App Namespace: 'blog-api'
"""
from django.urls import path
from . views import (
    SubscriptionPlansList,
    CreateCheckOutSession,
    stripe_webhook_view,
)

# pylint: disable=invalid-name
app_name = 'subscriptions-api'

urlpatterns = [
    path("list/", SubscriptionPlansList.as_view(), name='list'),
    path("checkout/<int:pk>/", CreateCheckOutSession.as_view(), name='checkout-subscription-payment'),
    path('webhook-endpoint/', stripe_webhook_view)
]
