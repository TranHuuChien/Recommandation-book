from django.urls import path
from .views import SaveComment, SaveChildComment, BookRankings, SaveLike, FavouriteBooks, AddFavourite, BooksSearch, BooksNew, SubmitRating, ShareBook
from .views import check_like_book, add_comment, get_comments, check_favourite_book
app_name = 'book'
urlpatterns = [
    path('save_comment', SaveComment.as_view(), name='save_comment'),
    path('save_child_comment', SaveChildComment.as_view(), name='save_child_comment'),
    path('ranking', BookRankings.as_view(), name='ranking'),
    path('favourite', FavouriteBooks.as_view(), name='favourite'),
    path('like/<int:book_id>/', SaveLike.as_view(), name='like_book'),
    path('check_like_book/<int:book_id>/', check_like_book, name='check_like_book'),
    path('add-comment/<int:book_id>/', add_comment, name='add-comment'),
    path('get-comments/<int:book_id>/', get_comments, name='get-comments'),
    path('check_favourite_book/<int:book_id>/', check_favourite_book, name='check_favourite_book'),
    path('add_favourite/<int:book_id>/', AddFavourite.as_view(), name='add_favourite'),
    path('search', BooksSearch.as_view(), name='search'),
    path('booksnew/<int:page>/', BooksNew.as_view(), name='booksnew'),
    path('submit_rating/<int:book_id>/', SubmitRating.as_view(), name='submit_rating'),
    path('share_book', ShareBook.as_view(), name='shareBook'),
]