from django.contrib import admin
from .models.models import Chapter, ReadingHistory, NotificationChapter

# Register your models here.
admin.site.register(Chapter)
admin.site.register(ReadingHistory)
admin.site.register(NotificationChapter)
