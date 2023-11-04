from django.urls import path
from .views import HomeView,Detail, DownloadPDFView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('detail/<slug:book_slug>', Detail.as_view(), name='detail'),
    path('download-pdf/<int:book_id>/', DownloadPDFView.as_view(), name='download_pdf'),
]