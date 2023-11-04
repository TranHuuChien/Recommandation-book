from django.urls import path
from .views import ChapterView, ReadingHistoryView

app_name = 'chapter'
urlpatterns = [
    path('<slug:book_slug>/<slug:chapter_slug>', ChapterView.as_view(), name='chapter_by_slug'),
    path('reading_history', ReadingHistoryView.as_view(), name='reading_history'),
]