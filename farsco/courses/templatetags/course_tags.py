# courses/templatetags/course_tags.py
from django import template

register = template.Library()

@register.filter
def get_range(value):
    return range(value)