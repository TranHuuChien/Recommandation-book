from django.shortcuts import render
from django.views import View
from book.models.models import Book
from genre.models.models import Genre

# Create your views here.
class GenreView(View):
    def get(self, request, genre_slug):
        books = Book.objects.filter(genre__genre_slug = genre_slug)
        context = {'books':books}
        return render(request, 'homepage/genre.html', context)