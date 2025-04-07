# main/urls.py
from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import (
    HomeView,
    AboutView,
    ContactView,
    ServicesView,
    LoadingView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServicesView.as_view(), name='services'),
    path('loading/', LoadingView.as_view(), name='loading'),
    
    # Password reset URLs
    path('password-reset/', 
         PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/', 
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]