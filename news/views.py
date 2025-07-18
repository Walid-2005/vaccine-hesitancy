"""
Views for the news section of the Vaccine Hesitancy WebApp.

Includes:
- Listing recent news articles from the database
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import News


def news(request):
    """
    Display the 3 most recent news articles.

    Retrieves and renders news items ordered by most recent creation date.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with news items.
    """
    # Query the 3 latest news entries from the News model
    news_items = News.objects.all().order_by('-created_at')[:3]

    # Render the news.html template with the context
    return render(request, 'pages/news.html', {'news_items': news_items})
