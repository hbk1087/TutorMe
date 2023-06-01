from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    path('createAccount/', views.createAccount, name='createAccount'),
    path('add_profile/', views.add_profile, name='add_profile'),
]