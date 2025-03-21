# accounts/urls.py
from django.urls import path
from .views import (
    # Remove these as they are now in main urls.py
    # CustomLoginView,
    # UserRegistrationView,
    CustomLogoutView,
    profile_view,
    dashboard_view
)

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
]