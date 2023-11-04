from django.db import models
from django.utils import timezone
from genre.models.models import Genre
from author.models.models import Author
from user.models.models import MyUser


# Create your models here.
class Book(models.Model):
    genre = models.ManyToManyField(Genre, related_name='book')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length=255, null=False, blank=False)
    status_choice = ((0,'Đang cập nhật'), (1,'Ngưng cập nhật'), (2,'Hoàn thành'))
    book_status_choice = models.IntegerField(choices=status_choice, default=0)
    book_description = models.TextField(default='')
    book_img = models.ImageField(blank=True, null=True)
    book_slug = models.CharField(max_length=100, null=False, blank=False, unique=True)
    book_view = models.IntegerField(default=0)
    book_rating = models.FloatField(default=0.0)
    book_status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())
    update_at = models.DateTimeField(auto_now=timezone.datetime.now())
    book_translator = models.CharField(max_length=100, null=True, blank=False)
    # Sách được viết bởi user
    #user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    #by_admin = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.book_name} - {self.author.author_name}'
    @property
    def ImageURL(self):
        try:
            url = self.book_img.url
        except:
            url = ''
        return url
    
class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.book.book_name} - {self.content[:20]}'

    def get_reply_comments(self):
        return Comment.objects.filter(parent_comment=self).order_by('created_at')

class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_like = models.BooleanField(null=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.book_name} - {self.is_like}'

class FavouriteBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=timezone.datetime.now())

    def __str__(self):
        return f'{self.user.username} - {self.book.book_name}'

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.book_name} - {self.rating}'
    

    





