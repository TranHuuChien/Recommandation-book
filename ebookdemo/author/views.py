from django.shortcuts import render
from django.views import View
from book.models.models import Book
from author.models.models import Author


# Create your views here.
class AuthorView(View):
    def get(self, request, author_slug):
        books = Book.objects.filter(author__author_slug = author_slug)
        context = {'books':books}
        return render(request, 'homepage/author.html', context)