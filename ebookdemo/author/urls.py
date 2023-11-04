from django.urls import path
from .views import AuthorView

app_name='author'
urlpatterns = [
    path('<slug:author_slug>', AuthorView.as_view(), name='author_by_slug'),
]