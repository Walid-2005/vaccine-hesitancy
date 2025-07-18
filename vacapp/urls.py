"""
URL configuration for vacapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define the main URL routing table
urlpatterns = [
    # Root-level URL patterns delegated to the 'pages' app
    path('', include('pages.urls')),

    # Also include root-level URLs from the 'news' app
    # Note: If both 'pages.urls' and 'news.urls' define the same path (e.g., ''), only one will be matched.
    path('', include('news.urls')),

    # Prefix all API endpoints with '/api/'
    path('api/', include('api.urls')),

    # Django admin interface
    path('admin/', admin.site.urls),
]

# Serve media files during development
# This maps MEDIA_URL to the MEDIA_ROOT directory
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
