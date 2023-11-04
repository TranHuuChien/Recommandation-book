from django.db import models
from django.utils import timezone

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=100, default='', unique=True)
    genre_description = models.CharField(max_length=255, default='')
    genre_slug = models.CharField(max_length=100, default='', unique=True)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    update_at = models.DateTimeField(auto_now=timezone.datetime.now())
    def __str__(self):
        return self.genre_name