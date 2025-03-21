# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', _('دانشجو')
        INSTRUCTOR = 'INSTRUCTOR', _('مدرس')
        STAFF = 'STAFF', _('کارمند فارسکو')
        
    # Basic user fields (name, email already in AbstractUser)
    phone_number = models.CharField(_('شماره تماس'), max_length=15, blank=True)
    role = models.CharField(
        _('نقش'),
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    
    # Profile image
    profile_image = models.ImageField(
        _('تصویر پروفایل'),
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    
    # Terms acceptance
    has_accepted_terms = models.BooleanField(_('پذیرش قوانین'), default=False)
    terms_accepted_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        
    def __str__(self):
        return self.get_full_name() or self.username
        
    def is_student(self):
        return self.role == self.Role.STUDENT
        
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR
        
    def is_farsco_staff(self):
        return self.role == self.Role.STAFF

# User profile for additional information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_('بیوگرافی'), blank=True)
    linkedin = models.URLField(_('پروفایل لینکدین'), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل‌ها')
        
    def __str__(self):
        return f"پروفایل {self.user.get_full_name() or self.user.username}"