# courses/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Course, 
    CourseCategory, 
    CourseLevel, 
    CourseModule,
    CourseEnrollment,
    CourseReview
)

class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'instructor', 'price', 
                    'duration_hours', 'rating', 'rating_count', 'is_active')
    list_filter = ('category', 'level', 'is_active', 'is_popular', 'is_new')
    search_fields = ('title', 'description', 'instructor__username', 
                     'instructor__first_name', 'instructor__last_name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseModuleInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'short_description', 
                      'category', 'level', 'instructor', 'thumbnail')
        }),
        (_('مشخصات دوره'), {
            'fields': ('price', 'duration_hours')
        }),
        (_('وضعیت'), {
            'fields': ('is_active', 'is_popular', 'is_new')
        }),
        (_('امتیازات'), {
            'fields': ('rating', 'rating_count'),
            'classes': ('collapse',)
        })
    )

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_enrolled', 'is_completed')
    list_filter = ('is_completed', 'date_enrolled')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 
                     'course__title')
    date_hierarchy = 'date_enrolled'

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 
                     'course__title', 'comment')
    date_hierarchy = 'created_at'