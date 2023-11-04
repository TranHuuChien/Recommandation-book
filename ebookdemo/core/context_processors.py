# Cấu hình để tự động hiển thị dữ liệu thể lên navbar
from genre.models.models import Genre  # Thay thế 'Genre' bằng tên model thể loại của bạn
from book.models.models import Book, FavouriteBook
from user.models.models import MyUser
from chapter.models.models import NotificationChapter

def genres(request):
    # Lấy danh sách thể loại từ cơ sở dữ liệu
    genres_list = Genre.objects.all()
    return {'genres_list': genres_list}

def topviews(request):
    # Lấy danh sách thể loại từ cơ sở dữ liệu
    books_views = Book.objects.order_by('-book_view')
    return {'books_views': books_views[0:10]}

def notification_chapter(request):
    # Lấy danh sách thông báo chương mới dành cho người đã theo dõi sách
    notifications_user = []
    try:
        user_id = request.session['id']
    except:
        user_id = 0
    if user_id > 0:
        user = MyUser.objects.get(pk=user_id)
        try:
            favorite_books = FavouriteBook.objects.filter(user_id=user_id)
            books = Book.objects.filter(id__in=favorite_books.values('book_id'))
            notifications_user=NotificationChapter.objects.filter(chapter__book__in=books).order_by('-create_at')
            print(notifications_user)
        except:
            notifications_user = None
    
    
    return {'notifications_user': notifications_user}
