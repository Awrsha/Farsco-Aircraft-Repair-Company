# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q, Min, Max, Avg
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.urls import reverse

from .models import Course, CourseCategory, CourseLevel, CourseEnrollment, CourseReview
from .forms import CourseReviewForm

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Apply filters
        category = self.request.GET.get('category')
        level = self.request.GET.get('level')
        duration = self.request.GET.get('duration')
        price_range = self.request.GET.get('price')
        search_query = self.request.GET.get('search')
        sort_by = self.request.GET.get('sort_by', 'popularity')
        
        # Category filter
        if category and category != 'all':
            queryset = queryset.filter(category__slug=category)
            
        # Level filter
        if level and level != 'all':
            queryset = queryset.filter(level__slug=level)
            
        # Duration filter
        if duration:
            if duration == 'short':
                queryset = queryset.filter(duration_hours__lt=100)
            elif duration == 'medium':
                queryset = queryset.filter(duration_hours__gte=100, duration_hours__lte=200)
            elif duration == 'long':
                queryset = queryset.filter(duration_hours__gt=200)
        
        # Price range filter
        if price_range:
            try:
                max_price = int(price_range)
                if max_price > 0:
                    queryset = queryset.filter(price__lte=max_price)
                else:
                    # Free courses
                    queryset = queryset.filter(price=0)
            except (ValueError, TypeError):
                pass
                
        # Search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(instructor__first_name__icontains=search_query) |
                Q(instructor__last_name__icontains=search_query)
            )
            
        # Sorting
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        else:  # Default: popularity
            queryset = queryset.order_by('-is_popular', '-rating', '-rating_count')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories and levels for filters
        context['categories'] = CourseCategory.objects.all()
        context['levels'] = CourseLevel.objects.all().order_by('order')
        
        # Get selected filters
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['selected_level'] = self.request.GET.get('level', 'all')
        context['selected_duration'] = self.request.GET.get('duration', 'all')
        context['selected_price'] = self.request.GET.get('price', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort_by', 'popularity')
        
        # Get price range for slider
        price_range = Course.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        
        context['min_price'] = price_range['min_price'] or 0
        context['max_price'] = price_range['max_price'] or 20000000  # Default max price
        
        # Count total courses
        context['total_courses'] = Course.objects.filter(is_active=True).count()
        
        # Add skeleton range for loading cards
        context['skeleton_range'] = range(3)
        
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Add review form
        context['review_form'] = CourseReviewForm()
        
        # Check if user is enrolled
        if self.request.user.is_authenticated:
            context['is_enrolled'] = CourseEnrollment.objects.filter(
                user=self.request.user,
                course=course
            ).exists()
            
            # Check if user has already reviewed
            context['has_reviewed'] = CourseReview.objects.filter(
                user=self.request.user,
                course=course
            ).exists()
            
            if context['has_reviewed']:
                context['user_review'] = CourseReview.objects.get(
                    user=self.request.user,
                    course=course
                )
        
        # Get related courses
        context['related_courses'] = Course.objects.filter(
            category=course.category,
            is_active=True
        ).exclude(pk=course.pk)[:3]
        
        return context

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Check if already enrolled
    if CourseEnrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, _('شما قبلاً در این دوره ثبت‌نام کرده‌اید.'))
    else:
        # Create enrollment
        CourseEnrollment.objects.create(user=request.user, course=course)
        messages.success(request, _('ثبت‌نام شما در دوره با موفقیت انجام شد.'))
    
    return redirect('courses:course_detail', slug=slug)

@login_required
def review_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Check if user is enrolled
    if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, _('برای ثبت نظر باید در دوره ثبت‌نام کرده باشید.'))
        return redirect('courses:course_detail', slug=slug)
    
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        
        if form.is_valid():
            # Check if user has already reviewed
            existing_review = CourseReview.objects.filter(
                user=request.user,
                course=course
            ).first()
            
            if existing_review:
                # Update existing review
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, _('نظر شما با موفقیت به‌روزرسانی شد.'))
            else:
                # Create new review
                review = form.save(commit=False)
                review.user = request.user
                review.course = course
                review.save()
                messages.success(request, _('نظر شما با موفقیت ثبت شد.'))
            
            # Update course rating
            course_reviews = CourseReview.objects.filter(course=course)
            avg_rating = course_reviews.aggregate(Avg('rating'))['rating__avg']
            
            course.rating = round(avg_rating, 1) if avg_rating else 0.0
            course.rating_count = course_reviews.count()
            course.save()
            
    return redirect('courses:course_detail', slug=slug)

# courses/views.py - Update the category_courses and level_courses functions
def category_courses(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug)
    # Update URL reversing to handle the namespace
    return redirect(f"/courses/?category={slug}")

def level_courses(request, slug):
    level = get_object_or_404(CourseLevel, slug=slug)
    # Update URL reversing to handle the namespace
    return redirect(f"/courses/?level={slug}")
    
@login_required
def my_courses(request):
    enrollments = CourseEnrollment.objects.filter(
        user=request.user
    ).select_related('course').order_by('-date_enrolled')
    
    return render(request, 'my_courses.html', {
        'enrollments': enrollments
    })

def filter_courses_ajax(request):
    """AJAX view for filtering courses"""
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    # Use the same filtering logic from CourseListView
    courses_view = CourseListView()
    courses_view.request = request
    courses = courses_view.get_queryset()
    
    # Prepare JSON response
    courses_data = []
    for course in courses[:20]:  # Limit to 20 results
        courses_data.append({
            'id': course.id,
            'title': course.title,
            'slug': course.slug,
            'short_description': course.short_description,
            'price': str(course.price),
            'formatted_price': course.formatted_price(),
            'thumbnail_url': course.thumbnail.url if course.thumbnail else None,
            'rating': float(course.rating),
            'rating_count': course.rating_count,
            'duration_hours': course.duration_hours,
            'instructor_name': f"{course.instructor.first_name} {course.instructor.last_name}",
            'category': course.category.name,
            'level': course.level.name,
            'level_slug': course.level.slug,
            'is_popular': course.is_popular,
            'is_new': course.is_new,
        })
    
    return JsonResponse({
        'courses': courses_data,
        'total': courses.count()
    })