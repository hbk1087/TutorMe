from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('sis_search/', views.sis_search, name='sis_search'),
    path('sis_form_submit/', views.sis_form_submit, name='sis_form_submit'),
    path('find_tutors/<str:crse_id>/', views.find_tutors, name='find_tutors'),
    path('request_tutor/<int:tutor_id>/<str:crse_id>', views.request_tutor, name='request_tutor'),
    path('show_requests', views.show_requests, name='show_requests'),
    path('schedule/', views.schedule, name='schedule'),
    path('update_profile', views.update_profile, name='update_profile')
]
