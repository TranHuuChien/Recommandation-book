from django.shortcuts import render
from django.views import View
from book.models.models import Book, Comment, Like, Rating
from genre.models.models import Genre
from chapter.models.models import Chapter, ReadingHistory
from author.models.models import Author
from user.models.models import MyUser
import pandas as pd
import pickle
from train.recommendation import Recommendation


model = pickle.load(open('colabbase/artifacts/model.pkl', 'rb'))
book_name = pickle.load(open('colabbase/artifacts/book_name.pkl', 'rb'))
final_rating = pickle.load(open('colabbase/artifacts/final_rating.pkl', 'rb'))
books_pivot = pickle.load(open('colabbase/artifacts/books_pivot.pkl', 'rb'))

def recommend_book(book_id):
    #book_id = np.where(books_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(books_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
    return suggestion
    # for i in suggestion:
    #   books = books_pivot.index[i]
    #   for j in books:
    #     print(j)

# Create your views here.
class HomeView(View):
    def get(self, request):
        books = Book.objects.all()
        set_book_id = set()
        set_book = list()
        set_book_create = Book.objects.raw("SELECT * FROM book_book order by create_at desc limit 8;")
        set_book_rating = Book.objects.raw("SELECT * FROM book_book order by book_rating desc limit 8;")

        if 'id' in request.session:
            user_id = request.session['id']
            str_head = "SELECT * FROM book_rating as r where r.user_id = "
            str_tail = " and r.rating>3 limit 3;"
            str_query = str_head + str(user_id) + str_tail
            l = list(Rating.objects.raw(str_query))
            for i in l:
                a = recommend_book(i.book_id)
                set_book_id.update(a[0])
            for b in books:
                if b.id in set_book_id:
                    set_book.append(b)
            print(set_book)
        else:
            set_book = Book.objects.raw("SELECT * FROM book_book order by update_at desc limit 8;")
        context = {'books': books, 'book_recommend': set_book,
                   'book_create': set_book_create, 'book_rating': set_book_rating}
        return render(request, 'homepage/index.html', context)
class Detail(View):
    def get(self, request, book_slug):
        book = Book.objects.get(book_slug = book_slug)
        genres = Genre.objects.filter(book__id = book.id)
        author = Author.objects.filter(book__id = book.id)[0]
        chapters = Chapter.objects.filter(book_id=book.id)

        chapters_five_lasted = Chapter.objects.filter(book_id=book.id).order_by('-id')[:5]

        like_count = Like.objects.filter(book=book).count()
        all_comments = Comment.objects.filter(parent_comment=None)  # Lấy tất cả bình luận không có bình luận cha

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
        
        try:
            user_id = request.session['id']
        except:
            user_id = 0
        reading_chapter = None
        if user_id > 0:
            user = MyUser.objects.get(pk=user_id)
            try:
                reading = ReadingHistory.objects.get(user=user, chapter__book=book)
                reading_chapter = reading.chapter
            except ReadingHistory.DoesNotExist:
                reading_chapter = None

        context = {'book':book, 'genres':genres, 'chapters':chapters
        , 'author':author, 'five_chapters':chapters_five_lasted, 'all_comments': all_comments
        , 'like_count':like_count, 'reading_chapter':reading_chapter, 'book_recommendation':book_recommendation }
        return render(request,'homepage/detail.html', context)
    
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from reportlab.lib.units import inch

class DownloadPDFView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize = letter, bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Courier", 14)

        textob.textLine(f'Tên sách: {book.book_name}')
        textob.textLine(f'Tên tác giả: {book.author.author_name}')

        lines = []

        chapters = Chapter.objects.filter(book=book)
        for chap in chapters:
            #textob.textLine(f'{chap.chapter_name}')
            lines.append(chap.chapter_name)
            contents = chap.chapter_content.split(' ')
            line = ''
            for i in range(0,len(contents)):
                line += (contents[i] + ' ')
                if i % 10 == 0:
                    lines.append(line)
                    line = ''
                elif i == (len(contents) - 1) :
                    lines.append(line)

        for i in range(0,len(lines)):
            textob.textLine(lines[i])
            if((i+1) % 30 == 0):
                c.drawText(textob)
                c.showPage()
                textob = c.beginText()
                textob.setTextOrigin(inch, inch)
                textob.setFont("Courier", 14)
            elif i == (len(lines) - 1) :
                c.drawText(textob)
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename=f'{book.book_name}.pdf')
    
