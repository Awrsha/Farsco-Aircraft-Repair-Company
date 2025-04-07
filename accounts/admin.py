# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_image')}),
        (_('نقش'), {'fields': ('role',)}),
        (_('قوانین و مقررات'), {'fields': ('has_accepted_terms', 'terms_accepted_date')}),
        (_('دسترسی‌ها'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخ‌های مهم'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.register(User, CustomUserAdmin)