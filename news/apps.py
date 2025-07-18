"""
App configuration for the news app in the Vaccine Hesitancy WebApp.

This module registers the app with Django and sets default model behavior.
"""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    Configuration class for the 'news' Django app.

    Attributes:
        default_auto_field (str): Type of primary key to use by default.
        name (str): Application name used in settings and imports.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
