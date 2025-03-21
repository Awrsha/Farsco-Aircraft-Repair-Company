# main/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from courses.models import Course, CourseCategory
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Featured courses for the home page
        context['featured_courses'] = Course.objects.filter(
            is_active=True
        ).order_by('-is_popular', '-created_at')[:3]
        
        # Service categories
        context['course_categories'] = CourseCategory.objects.annotate(
            course_count=Count('courses')
        ).filter(course_count__gt=0)
        
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def post(self, request, *args, **kwargs):
        """Process contact form submission"""
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Here you would typically process the form data
        # For example, send an email or save to database
        
        # Just render the template with a success message
        return render(request, 'contact.html', {
            'success': True,
            'message': 'پیام شما با موفقیت ارسال شد. در اسرع وقت با شما تماس خواهیم گرفت.'
        })

class ServicesView(TemplateView):
    template_name = 'services.html'

def handler404(request, exception=None):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def handler500(request, exception=None):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)

class LoadingView(TemplateView):
    template_name = 'loading.html'