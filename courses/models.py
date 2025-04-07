# courses/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import User

class CourseCategory(models.Model):
    name = models.CharField(_('نام دسته‌بندی'), max_length=100)
    slug = models.SlugField(_('اسلاگ'), max_length=100, unique=True)
    description = models.TextField(_('توضیحات'), blank=True)
    icon = models.CharField(_('آیکون'), max_length=50, blank=True, 
                           help_text=_('نام آیکون از Font Awesome'))
    
    class Meta:
        verbose_name = _('دسته‌بندی دوره')
        verbose_name_plural = _('دسته‌بندی‌های دوره')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('courses:category', kwargs={'slug': self.slug})

class CourseLevel(models.Model):
    name = models.CharField(_('نام سطح'), max_length=50)
    slug = models.SlugField(_('اسلاگ'), max_length=50, unique=True)
    description = models.TextField(_('توضیحات'), blank=True)
    order = models.PositiveSmallIntegerField(_('ترتیب نمایش'), default=0)
    
    class Meta:
        verbose_name = _('سطح دوره')
        verbose_name_plural = _('سطوح دوره')
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(_('عنوان دوره'), max_length=200)
    slug = models.SlugField(_('اسلاگ'), max_length=200, unique=True)
    description = models.TextField(_('توضیحات'))
    short_description = models.CharField(_('توضیح کوتاه'), max_length=300)
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name=_('دسته‌بندی')
    )
    level = models.ForeignKey(
        CourseLevel,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name=_('سطح دوره')
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        verbose_name=_('مدرس')
    )
    thumbnail = models.ImageField(
        _('تصویر دوره'),
        upload_to='course_thumbnails/',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        _('قیمت دوره (تومان)'),
        max_digits=12,
        decimal_places=0,
        default=0
    )
    duration_hours = models.PositiveIntegerField(_('طول دوره (ساعت)'))
    is_popular = models.BooleanField(_('پرطرفدار'), default=False)
    is_new = models.BooleanField(_('جدید'), default=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ به‌روزرسانی'), auto_now=True)
    
    # Rating fields
    rating = models.DecimalField(
        _('امتیاز'), 
        max_digits=2, 
        decimal_places=1, 
        default=0.0
    )
    rating_count = models.PositiveIntegerField(_('تعداد نظرات'), default=0)
    
    class Meta:
        verbose_name = _('دوره')
        verbose_name_plural = _('دوره‌ها')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})
    
    def formatted_price(self):
        """Return formatted price with commas"""
        return f"{int(self.price):,}"

class CourseModule(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name=_('دوره')
    )
    title = models.CharField(_('عنوان ماژول'), max_length=200)
    description = models.TextField(_('توضیحات'), blank=True)
    order = models.PositiveSmallIntegerField(_('ترتیب نمایش'), default=0)
    
    class Meta:
        verbose_name = _('ماژول دوره')
        verbose_name_plural = _('ماژول‌های دوره')
        ordering = ['course', 'order']
        
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CourseEnrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('کاربر')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('دوره')
    )
    date_enrolled = models.DateTimeField(_('تاریخ ثبت‌نام'), auto_now_add=True)
    is_completed = models.BooleanField(_('تکمیل شده'), default=False)
    
    class Meta:
        verbose_name = _('ثبت‌نام دوره')
        verbose_name_plural = _('ثبت‌نام‌های دوره')
        unique_together = ['user', 'course']
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title}"

class CourseReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_reviews',
        verbose_name=_('کاربر')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('دوره')
    )
    rating = models.PositiveSmallIntegerField(_('امتیاز'), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_('نظر'))
    created_at = models.DateTimeField(_('تاریخ ثبت'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('نظر دوره')
        verbose_name_plural = _('نظرات دوره')
        unique_together = ['user', 'course']
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title} - {self.rating}/5"