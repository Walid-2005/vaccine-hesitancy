"""
Model definition for the News section of the Vaccine Hesitancy WebApp.

Stores article metadata such as title, description, image, and publication timestamp.
"""

from django.db import models


class News(models.Model):
    """
    Represents a news article displayed in the public news feed.

    Fields:
        title (str): Headline of the news item.
        description (str): Main body or summary of the article.
        image (ImageField): Associated visual (stored in `news_images/`).
        created_at (DateTime): Timestamp of article creation.
    """

    title = models.CharField(max_length=255)  # Article title
    description = models.TextField()  # Full article description or summary
    image = models.ImageField(upload_to='news_images/')  # Uploaded image path
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set creation timestamp

    def __str__(self):
        """
        Returns a human-readable string representation of the news article.
        """
        return self.title
