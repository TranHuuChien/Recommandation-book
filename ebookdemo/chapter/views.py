from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models.models import Chapter, ReadingHistory
from book.models.models import Book
from user.models.models import MyUser
from train.recommendation import Recommendation
import pickle
import pandas as pd
# Create your views here.
class ChapterView(View):
    def get(self,request,book_slug,chapter_slug):
        book = Book.objects.get(book_slug = book_slug)
        chapter = Chapter.objects.filter(book__book_slug=book_slug, chapter_slug=chapter_slug)[0]
        contents = chapter.chapter_content.split('.')
        chapters = Chapter.objects.filter(book__book_slug=book_slug)

        Recommendation.get_recommendations(book.book_name)
        print('Sach hien tai : '+book.book_name)
        # Lay ds sach duoc de xuat
        list_book = pickle.load(open('./train/books.pkl', 'rb'))
        list_book = pd.DataFrame(list_book)
        list_book_id = [] # mang chua danh sach de xuat
        for idx in list_book.index:
            #print(list_book['book_id'][idx])
            list_book_id.append(list_book['id'][idx])

        book_recommendation= []
        for idx in list_book_id:
            print(idx)
            book_recom  = Book.objects.get(pk = idx)
            book_recommendation.append(book_recom)
            print(book_recom.book_name)

        user_id = request.session['id']
        if user_id > 0:
            user = MyUser.objects.get(pk=user_id)
            try:
                reading = ReadingHistory.objects.get(user=user, chapter__book=book)
                reading.chapter = chapter
                reading.save()
            except ReadingHistory.DoesNotExist:
                ReadingHistory.objects.create(user=user, chapter=chapter)

        context = {'chapter': chapter, 'contents': contents, 'chapters':chapters, 'book':book,'book_recommendation':book_recommendation}
        return render(request, 'homepage/chapter.html', context)

class ReadingHistoryView(View):
    def get(self, request):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        reading_books = ReadingHistory.objects.filter(user=user).order_by('-create_at')
        context = {'reading_books':reading_books, 'title':'Lịch sử đọc'}
        return render(request, 'homepage/reading_history.html', context)
