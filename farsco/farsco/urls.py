# farsco/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomLoginView, UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Direct login and registration routes - fixed name to match template
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),  # Changed from 'register' to 'registration'
    
    # App URLs
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'main.views.handler404'