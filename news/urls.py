"""
URL configuration for the news app.

Defines route(s) for accessing the news section of the Vaccine Hesitancy WebApp.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Route to display latest news articles
    path('news', views.news, name='news'),
]
