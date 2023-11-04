from django.urls import path
from .views import GenreView

app_name='genre'
urlpatterns = [
    path('<slug:genre_slug>', GenreView.as_view(), name='genre_by_slug'),
]