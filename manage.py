"""
Main entry point for Django administrative tasks.

This script sets the default Django settings module and invokes the command-line
utility for various Django administrative operations such as running the development
server, applying migrations, or starting a new app.

Example usage:
    python manage.py runserver
    python manage.py makemigrations
"""

import os
import sys

def main():
    """
    Configure the Django environment and execute the appropriate management command.

    This function sets the default settings module for the Django project,
    handles ImportError exceptions if Django is not installed, and delegates
    command-line arguments to Django's management utility.
    """
    # Set the default Django settings module (used when DJANGO_SETTINGS_MODULE is not already defined)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacapp.settings')

    try:
        # Import the Django CLI execution utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an informative error if Django is not installed or accessible
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Delegate command-line arguments to Django’s command handler
    execute_from_command_line(sys.argv)

# Call the main function only when run as a script (not when imported)
if __name__ == '__main__':
    main()
