from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'tutors'
urlpatterns = [
    path('', views.index, name='index'),
    path('sis_search/', views.sis_search, name='sis_search'),
    path('sis_form_submit/', views.sis_form_submit, name='sis_form_submit'),
    path('add_course/<int:course_id>/', views.add_course, name='add_course'),
    path('show_requests', views.show_requests, name='show_requests'),
    path('schedule/', views.schedule, name='schedule'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('show_requests/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('show_requests/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    path('session/<int:request_id>/', views.session, name='session'),
    path('make_session/<int:request_id>/', views.make_session, name='make_session'),
]