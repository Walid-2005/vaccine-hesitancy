"""
WSGI configuration module for the vacapp Django project.

This module configures the WSGI application object required to serve the project
using a WSGI-compatible web server (e.g., Gunicorn, uWSGI, or mod_wsgi).

Attributes:
    application (WSGIHandler): The WSGI callable used by Django's servers and external WSGI servers.

Usage:
    This file is typically used as the entry point for deployment with WSGI servers.

References:
    https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for Django when WSGI loads the app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacapp.settings')

# Create the WSGI application object for the project
# This object will be used by any WSGI server (e.g., Gunicorn, uWSGI)
application = get_wsgi_application()
