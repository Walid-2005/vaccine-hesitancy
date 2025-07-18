import os
import sys

# Add your Django project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set the settings module for Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'vacapp.settings'

import django
django.setup()

# -- Project information
project = 'VaccineHesitancyWebApp'
author = 'Ameen Ahmed Shareef'
release = '1.0'

# -- General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # for Google/NumPy-style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output
html_theme = "furo"
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"
html_static_path = ['_static']
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
}