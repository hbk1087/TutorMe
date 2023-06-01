from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
import datetime
import requests
from django.contrib.auth.models import User
from login.models import Tutor, Student, Request, Course, Session

import requests,json
# Create your views here.
def index(request):
    return render(request, 'students/index.html')

def sis_search(request):
    return render(request, 'students/sis_search.html')

def get_or_create_course(crse_id, subject, catalog_nbr):
    try:
        course = Course.objects.get(crse_id=crse_id)
    except Course.DoesNotExist:
        course =  Course.objects.create(crse_id=crse_id, subject=subject, catalog_nbr=catalog_nbr)
    return course

def sis_form_submit(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        term = request.GET.get('term')
        subject = request.GET.get('subject')
        catalog_nbr = request.GET.get('catalog_nbr')
        instructor_name = request.GET.get('instructor_name')
        url = url_creator(year, term, subject, catalog_nbr, instructor_name)
        results = search(url)
        results_dict = {'results' : results}
        courses = []
        for res in results_dict['results']:
            course = get_or_create_course(res['crse_id'], res['subject'], res['catalog_nbr'])
            if course not in courses:
                courses.append(course)
        results_dict['courses'] = courses
        results_dict['data'] = [{'year':year, 'term':term, 'subject':subject, 'catalog_nbr':catalog_nbr,'instructor_name': instructor_name}]
    return render(request, 'students/sis_search.html', results_dict)



def url_creator(year, term, subject, catalog_nbr, instructor_name):
    base_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    if year != '':
        term_num = '1'
        if(term == 'spring'):
            term_num = '2'
        if(term_num == 'summer'):
            term_num = '6'
        if(term == 'fall'):
            term_num = '8'
        base_url += '&term=1' + year[-2:] + term_num
    if subject != '':
        base_url += '&subject=' + str(subject).upper();
    if catalog_nbr != '':
        base_url += '&catalog_nbr=' + str(catalog_nbr)
    if instructor_name != '':
        base_url += '&instructor_name=' + str(instructor_name).lower()
    return base_url

def search(url):
    r = requests.get(url)
    for c in r.json():
        print(c['subject'], c['catalog_nbr'], c['instructors'])
    return r.json()


def find_tutors(request, crse_id):
    tutors = Tutor.objects.filter(courses__crse_id=crse_id)
    context = {
        'crse_id': crse_id,
        'tutors':tutors,
    }
    return render(request, 'students/find_tutors.html', context)

# def get_course_description_by_crse_id(crse_id):
#     base_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
#     r = requests.get(base_url)
#     for c in r.json():
#         if c['crse_id'] == crse_id:
#             return c['descr']
#     descr = r.json()[0]['descr']
#     return descr

def request_tutor(request, crse_id, tutor_id):
    student = request.user.profile.student
    tutor = get_object_or_404(Tutor, id=tutor_id)
    course = Course.objects.filter(crse_id = crse_id)[0]
    existing_request = Request.objects.filter(student=student, tutor=tutor, course=course).exists()
    if existing_request:
        return find_tutors(request, crse_id)
    else:
        # Create a new tutor request
        tutor_request = Request(student=student, tutor=tutor, course=course)
        tutor_request.save()
    return render(request, 'students/sis_search.html')

def show_requests(request):
    student = request.user.profile.student
    requests = Request.objects.filter(student=student)
    context = {
        'requests':requests,
    }
    return render(request, 'students/show_requests.html', context)

def schedule(request):
    user_sessions = Session.objects.filter(student=request.user.profile.student)
    context = {
        'sessions': user_sessions
    }
    return render(request, 'students/schedule.html', context)

def update_profile(request):
    student = request.user.profile.student
    student.profile.first_name = request.GET.get('first_name')
    student.profile.last_name = request.GET.get('last_name')
    student.about_me = request.GET.get('about_me')
    student.save()
    return render(request, 'students/index.html')
