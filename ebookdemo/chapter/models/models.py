from django.db import models
from django.utils import timezone
from book.models.models import Book
from user.models.models import MyUser

# Create your models here.
class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=255, null=True, blank=False, unique=True)
    chapter_content = models.TextField(null=False, blank=False)
    chapter_slug = models.CharField(max_length=100, null=False, blank=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    update_at = models.DateTimeField(auto_now=timezone.datetime.now())

    def __str__(self):
        return f'{self.book.book_name} - {self.chapter_name}'

class ReadingHistory(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    update_at = models.DateTimeField(auto_now=timezone.datetime.now())

    def __str__(self):
        return f'{self.user.username} - {self.chapter.book.book_name} - {self.chapter.chapter_name}'


class NotificationChapter(models.Model): #Thông báo khi có chương mới
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    notification_content = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    update_at = models.DateTimeField(auto_now=timezone.datetime.now())

    def __str__(self):
        return f'{self.chapter.book.book_name} - {self.chapter.chapter_name} - {self.notification_content}'