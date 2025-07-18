"""
URL configuration for the pages app in the Vaccine Hesitancy WebApp.

This module defines all route-to-view mappings, including:
- Home and survey views
- Prediction API
- Admin dashboard
- Login/logout
- Data viewing and Excel export

Imported Views:
    - index
    - survey_view
    - result_view
    - predict_hesitancy (from api.views)
    - admin_dashboard
"""

from django.urls import path
from api.views import predict_hesitancy  # API endpoint for ML prediction
from .views import (
    survey_view,
    result_view,
    index,
    data,
    login,
    user_logout,
    download_excel,
    admin_dashboard
)

urlpatterns = [
    # Home page
    path('', index, name='index'),

    # Survey form page
    path('survey/', survey_view, name='survey'),

    # Prediction API endpoint (calls ML model)
    path('predict/', predict_hesitancy, name='predict_hesitancy'),

    # Authenticated data view for submitted responses
    path('data', data, name='data'),

    # Custom login/logout views
    path('login', login, name='login'),
    path('logout', user_logout, name='logout'),

    # Admin-only export of all survey results to Excel
    path('download_excel/', download_excel, name='download_excel'),

    # Admin dashboard with graphs/statistics
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    # Analytics endpoints (commented out but may be reactivated later)
    # path('analytics_data/', views.analytics_data, name='analytics_data'),
    # path('heatmap_data/', views.heatmap_data, name='heatmap_data'),
    # path('correlation_data/', views.correlation_data, name='correlation_data'),
    # path('pie_chart_data/', views.pie_chart_data, name='pie_chart_data'),
]
