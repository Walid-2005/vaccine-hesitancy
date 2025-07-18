"""
App configuration for the api module of the Vaccine Hesitancy WebApp.

Registers the app and sets default field behavior for model primary keys.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the 'api' Django app.

    Attributes:
        default_auto_field (str): Specifies default field type for primary keys.
        name (str): The full Python path to the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
