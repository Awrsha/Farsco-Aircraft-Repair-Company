# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import messages

from .forms import (
    CustomAuthenticationForm, 
    CustomUserCreationForm,
    ProfileUpdateForm,
    UserUpdateForm
)
from .models import User

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Set session expiry to 0 seconds if remember_me is False
            self.request.session.set_expiry(0)
            # Session will expire when browser is closed
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserRegistrationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            _('ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد حساب کاربری خود شوید.')
        )
        return response
        
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('پروفایل شما با موفقیت به‌روزرسانی شد.'))
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'profile.html', context)

@login_required
def dashboard_view(request):
    # This will return dashboard based on user role
    user = request.user
    
    if user.is_student():
        return render(request, 'dashboard/student_dashboard.html')
    elif user.is_instructor():
        return render(request, 'dashboard/instructor_dashboard.html')
    elif user.is_farsco_staff() or user.is_staff:
        return render(request, 'dashboard/staff_dashboard.html')
    else:
        return render(request, 'dashboard/dashboard.html')