"""
Form definition for creating and editing News items in the admin or dashboard interface.
"""

from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    """
    Form for creating and updating News articles.

    Includes:
        - title (CharField)
        - description (TextField)
        - image (ImageField)
    """

    class Meta:
        model = News
        fields = ['title', 'description', 'image']
