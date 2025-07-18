"""
URL configuration for the api app.

Defines endpoint(s) for machine learning model prediction.
"""

from django.urls import path
from .views import predict_hesitancy

urlpatterns = [
    # Endpoint for predicting vaccine hesitancy from latest survey data
    path('predict/', predict_hesitancy, name="predict_hesitancy"),
]
