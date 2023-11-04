from django.urls import path
from .views import LoginView, RegisterView, LogoutView, AccountView, ChangePassword

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('account', AccountView.as_view(), name='account'),
    path('change-password', ChangePassword.as_view(), name='change-password'),
]