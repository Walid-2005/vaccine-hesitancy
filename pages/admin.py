"""
Admin configuration for managing RespondentsInfo and Responses models
in the Django admin interface of the Vaccine Hesitancy WebApp.
"""

from django.contrib import admin
from .models import RespondentsInfo, Responses


class RespondentsInfoAdmin(admin.ModelAdmin):
    """
    Admin interface customization for RespondentsInfo model.

    Displays all fields in the list view, enables sorting, searching, and filtering.
    """
    list_display = [field.name for field in RespondentsInfo._meta.fields]  # Display all model fields
    ordering = ['user_id']  # Default ordering by primary key
    search_fields = ['user_id', 'age', 'sex', 'marital_status', 'qualification', 'job']  # Enable search
    list_filter = ['age', 'sex', 'marital_status', 'qualification', 'job']  # Enable sidebar filters


class ResponsesAdmin(admin.ModelAdmin):
    """
    Admin interface customization for Responses model.

    Enables efficient display and filtering of question responses.
    """
    list_display = [field.name for field in Responses._meta.fields]  # Show all fields in admin table
    ordering = ['user_id']  # Order by respondent ID
    search_fields = ['user_id', 'question1']  # Allow admin to search responses
    list_filter = ['question1']  # Sidebar filter for one sample question
    raw_id_fields = ['user_id']  # Use raw ID input for foreign key to optimize admin load


# Register the models with their respective custom admin configurations
admin.site.register(RespondentsInfo, RespondentsInfoAdmin)
admin.site.register(Responses, ResponsesAdmin)
