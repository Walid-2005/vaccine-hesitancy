"""
App configuration for the pages module in the Vaccine Hesitancy WebApp.

This file registers the app with Django and sets default field behavior for models.
"""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """
    Configuration class for the 'pages' Django app.

    Attributes:
        default_auto_field: Specifies the type of primary key to use by default.
        name: The name of the Django app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
