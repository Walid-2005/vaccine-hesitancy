"""
Admin configuration for the news app.

Registers the News model for management through the Django admin interface.
"""

from django.contrib import admin
from .models import News

# Register the News model so it appears in the admin dashboard
admin.site.register(News)
