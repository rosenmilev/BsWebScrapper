from django.contrib.auth.models import User
from django.db import models


class ScrapedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_url = models.URLField()
    scraped_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)