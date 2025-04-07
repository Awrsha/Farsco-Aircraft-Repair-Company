# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import User, Profile

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_('نام کاربری یا ایمیل'),
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )
    
    password = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(attrs={'placeholder': ' '})
    )
    
    remember_me = forms.BooleanField(
        label=_('مرا به خاطر بسپار'),
        required=False,
        initial=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

# accounts/forms.py - Update the CustomUserCreationForm
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('نام'),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )
    
    last_name = forms.CharField(
        label=_('نام خانوادگی'),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )
    
    username = forms.CharField(
        label=_('نام کاربری'),
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )
    
    email = forms.EmailField(
        label=_('آدرس ایمیل'),
        widget=forms.EmailInput(attrs={'placeholder': ' '})
    )
    
    phone_number = forms.CharField(
        label=_('شماره تماس'),
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )
    
    password1 = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(attrs={'placeholder': ' '})
    )
    
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput(attrs={'placeholder': ' '})
    )
    
    role = forms.ChoiceField(
        label=_('نقش شما'),
        choices=User.Role.choices,
        initial=User.Role.STUDENT,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    has_accepted_terms = forms.BooleanField(
        label=_('قوانین و مقررات و حریم خصوصی فارسکو را می‌پذیرم'),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'phone_number', 'password1', 'password2', 
            'role', 'has_accepted_terms'
        ]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if user.has_accepted_terms:
            user.terms_accepted_date = timezone.now()
        
        if commit:
            user.save()
            # Remove this line - let the signal handler create the profile
            # Profile.objects.create(user=user)
            
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'linkedin']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']