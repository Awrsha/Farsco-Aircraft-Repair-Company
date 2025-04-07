# courses/management/commands/load_initial_data.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from courses.models import CourseCategory, CourseLevel

class Command(BaseCommand):
    help = 'Loads initial data for the Farsco application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Create course categories
        categories = [
            {'name': 'مکانیک هواپیما', 'icon': 'fa-cogs'},
            {'name': 'اویونیک', 'icon': 'fa-microchip'},
            {'name': 'موتور هواپیما', 'icon': 'fa-engine'},
            {'name': 'سازه و بدنه', 'icon': 'fa-plane'},
            {'name': 'ایمنی پرواز', 'icon': 'fa-shield-alt'},
        ]
        
        for cat_data in categories:
            CourseCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'icon': cat_data['icon']
                }
            )
        
        # Create course levels
        levels = [
            {'name': 'مقدماتی', 'order': 1},
            {'name': 'متوسط', 'order': 2},
            {'name': 'پیشرفته', 'order': 3},
            {'name': 'تخصصی', 'order': 4},
        ]
        
        for level_data in levels:
            CourseLevel.objects.get_or_create(
                name=level_data['name'],
                defaults={
                    'slug': slugify(level_data['name']),
                    'order': level_data['order']
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))