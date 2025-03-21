# courses/urls.py
from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    enroll_course,
    review_course,
    category_courses,
    level_courses,
    my_courses,
    filter_courses_ajax
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('my-courses/', my_courses, name='my_courses'),
    path('category/<slug:slug>/', category_courses, name='category'),
    path('level/<slug:slug>/', level_courses, name='level'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/enroll/', enroll_course, name='enroll'),
    path('<slug:slug>/review/', review_course, name='review'),
    path('api/filter/', filter_courses_ajax, name='filter_courses_ajax'),
]