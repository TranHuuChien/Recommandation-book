from django.shortcuts import render, redirect
from django.views import View
from user.models.models import MyUser
from .models.models import Book, Comment, Like, FavouriteBook, Rating
from datetime import date
from django.db.models import F, Sum
from django.http import JsonResponse

from subprocess import call
#send mail
from django.core.mail import send_mail
from django.conf import settings

#paging
from .paging import PagingInfo, BooksPaging

#request login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login, decorators

# Create your views here.

class SaveComment(View):
    def post(self, request):
        content = request.POST.get('content')
        book_id = request.POST.get('book_id')
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
        comment = Comment.objects.create(book=book, user=user, content=content)
        return redirect('/detail/'+book.book_slug)
    
class SaveChildComment(View):
    def post(self, request):
        content = request.POST.get('content')
        book_id = request.POST.get('book_id')
        parent_id = request.POST.get('parent_id')
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
        parent_comment = Comment.objects.get(pk=parent_id)
        comment = Comment.objects.create(book=book, user=user, content=content, parent_comment=parent_comment)

        print(comment)
        return redirect('/detail/'+book.book_slug)
    
class BookRankings(View):
    def get(self, request, time='day'):
        context = {}
        if time == 'day':
            today = date.today()
            books_by_views_today = Book.objects.order_by('-book_view')
            context = {'books_ranking':books_by_views_today, 'title': 'Bảng xếp hạng'}
            print(books_by_views_today)

        if time == 'month':
            current_month = date.today().month
            books_by_views_this_month = Book.objects.filter(create_at__month=current_month).annotate(total_views=Sum('book_view'))
            context = {'books_ranking':books_by_views_this_month}
        if time == 'year':
            current_year = date.today().year
            books_by_views_this_year = Book.objects.filter(create_at__year=current_year).annotate(total_views=Sum('book_view'))
            context = {'books_ranking':books_by_views_this_year}
        

        
        return render(request, 'homepage/ranking.html', context)

    
class SaveLike(View):
    def post(self,request, book_id):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        try:
            like = Like.objects.get(user=user, book_id=book_id)
            like.delete()  # Nếu đã "like" thì xóa
            liked = False
        except Like.DoesNotExist:
            Like.objects.create(user=user, book_id=book_id, is_like=True)
            liked = True

        like_count = Like.objects.filter(book__id=book_id).count()
        print(like_count)

        return JsonResponse({'liked': liked, 'like_count':like_count})

#Kiểm tra người dùng đã like hay chưa
def check_like_book(request, book_id):
    user_id = request.session['id']
    user = MyUser.objects.get(pk=user_id)
    try:
        liked = Like.objects.get(user=user, book_id=book_id)
        liked = True  # Người dùng đã "like"
    except Like.DoesNotExist:
        liked = False  # Người dùng chưa "like"

    return JsonResponse({'liked': liked})

def add_comment(request, book_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        user_id = request.session['id']
        print(book_id, user_id, content)
        user = MyUser.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
        comment = Comment.objects.create(book=book, user=user, content=content)
        comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_comments(request, book_id):
    comments = Comment.objects.filter(book_id=book_id)
    #comments_data = [{'text': comment.content, 'username': comment.user.username, 'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M:%S")} for comment in comments]
    comments_data = []
    for comment in comments:
        is_myuser = False
        if comment.user.id == request.session['id']:
            is_myuser = True
        data = {'id':comment.id, 'text': comment.content, 'username': comment.user.username, 'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'is_myuser':is_myuser}
        comments_data.append(data)
    #Thiếu phần reply comment
    return JsonResponse({'comments': comments_data})

class FavouriteBooks(LoginRequiredMixin,View):
    login_url = "users:login"
    def get(self, request):
        user_id = request.session['id']
        favorite_books = FavouriteBook.objects.filter(user__id = user_id)
        context = {'favorite_books':favorite_books}
        print(favorite_books)
        return render(request, 'homepage/favourite.html', context)
    
class AddFavourite(View):
    def post(self,request, book_id):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        try:
            favourite = FavouriteBook.objects.get(user=user, book_id=book_id)
            favourite.delete() 
            favourited = False
        except FavouriteBook.DoesNotExist:
            FavouriteBook.objects.create(user=user, book_id=book_id)
            favourited = True

        return JsonResponse({'favourited': favourited})
    
#Kiểm tra người dùng đã đánh dấu hay chưa
def check_favourite_book(request, book_id):
    user_id = request.session['id']
    user = MyUser.objects.get(pk=user_id)
    try:
        favourited = FavouriteBook.objects.get(user=user, book_id=book_id)
        favourited = True
    except FavouriteBook.DoesNotExist:
        favourited = False

    return JsonResponse({'favourited': favourited})

class BooksSearch(View):
    def get(self, request):
        keywords = request.GET.get('keywords')
        books_search = Book.objects.filter(book_name__contains=keywords) | Book.objects.filter(author__author_name__contains=keywords) | Book.objects.filter(genre__genre_name__contains=keywords)
        context = {'books':books_search, 'title':'Tìm kiếm theo từ khóa : '+ keywords}
        return render(request, 'homepage/new_book.html', context)
    
class BooksNew(View):
    def get(self, request, page=1):
        books_new = Book.objects.order_by('-create_at')
        pageSize = 6
        #pageSize = 2
        paging = PagingInfo(pageSize=pageSize,pageCurrent=page,pageCount=books_new.count())
        first = (page-1)*pageSize
        books_now_page = Book.objects.order_by('-create_at')[first:first+pageSize]
        booksPaging = BooksPaging(paging=paging, books=books_now_page)
        totalPage = list(range(1,paging.totalPage+1))
        context = {'booksPaging':booksPaging, 'totalPage':totalPage,'title':'Sách mới nhất'}
        
        #books_new = Book.objects.order_by('-create_at')
        #context = {'books':books_new, 'title':'Sách mới nhất'}
        return render(request, 'homepage/new_book.html', context)

#Gửi điểm rating về server
class SubmitRating(View):
    def get(self,request, book_id):
        #book_id = request.GET.get('book_id')
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)
        try:
            rating = Rating.objects.get(user=user, book_id=book_id)
            print("Điểm rating user: " , rating.rating)
            return JsonResponse({'user_rating': rating.rating})
        except Rating.DoesNotExist:
            return JsonResponse({'user_rating': None})
        
    def post(self,request, book_id):
        user_id = request.session['id']
        user = MyUser.objects.get(pk=user_id)

        rating = request.POST.get('rating')
        try:
            rated = Rating.objects.get(user=user, book_id=book_id)
            rated.rating = rating 
            rated.save()
        except Rating.DoesNotExist:
            Rating.objects.create(user=user, book_id=book_id, rating=rating)
        return JsonResponse({'success': True})
    
#Share Book
class ShareBook(View):
    def post(self,request):
        message = request.POST['message']
        email = request.POST['email']
        name = request.POST['title']

        book_id = request.POST['book_id']
        book = Book.objects.get(pk=book_id)
        try:
            message = message + ' Click here ! ' + "http://127.0.0.1:8000/detail/"+book.book_slug
            send_mail(
                name,#title
                message,#Message
                'settings.EMAIL_HOST_USER',#sender email
                [email], #reciver email
                fail_silently=False
            )
        except:
            request.session['error_message'] = 'Chia sẻ sách không thành công. Vui lòng thử lại!'
            request.session['success_message'] = None

        request.session['success_message'] = 'Chia sẻ sách thành công!'
        request.session['error_message'] = None
        return redirect('/detail/'+book.book_slug)


