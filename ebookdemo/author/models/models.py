from django.db import models
from django.utils import timezone
from genre.models.models import Genre

class Author(models.Model):
    author_name = models.CharField(max_length=255, null=False, blank=False)
    author_slug = models.CharField(max_length=100, null=False, blank=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    
    def __str__(self):
        return self.author_name