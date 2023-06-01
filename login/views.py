from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile, Student, Tutor
# Create your views here.



def index(request):
    return render(request, 'login/index.html')

def createAccount(request):
    return render(request, 'login/createProfile.html')

# def add_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect('login/index.html')
#     else:
#         form = ProfileForm()
#     return render(request, 'login/index.html', {'form': form})

def add_profile(request):
    if request.method == 'POST':

        profile = Profile()
        profile.user = request.user
        if request.POST['is_student'] == 'True':
            profile.is_student = True
        else:
            profile.is_student = False
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        #profile.student_major = request.POST['student_major']
        profile.save()
        if profile.is_student == True:
            print('Student Created')
            student = Student()
            student.profile = profile
            student.save()
        else:
            print('Tutor Created')
            tutor = Tutor()
            tutor.profile = profile
            tutor.pay_rate = 15
            tutor.crse_ids = ['006903']
            tutor.save()
    return HttpResponseRedirect(reverse('login:index'))


def profile_exists(request):
    try:
        profile = request.user.profile
        profile_exists = True
    except Profile.DoesNotExist:
        profile_exists = False
    return profile_exists