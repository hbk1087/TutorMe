from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
import requests
from datetime import datetime
from django.contrib.auth.models import User
from login.models import Tutor, Student, Request, Course, Session
from .calendar_api import test_calendar

# Create your views here.
def index(request):
    return render(request, 'tutors/index.html')

def sis_search(request):
    return render(request, 'tutors/sis_search.html')

def show_requests(request):
    tutor = request.user.profile.tutor
    requests = Request.objects.filter(tutor=tutor)
    context = {
        'requests':requests,
    }
    return render(request, 'tutors/show_requests.html', context)

def schedule(request):
    user_sessions = Session.objects.filter(tutor=request.user.profile.tutor)
    context = {
        'sessions': user_sessions
    }
    return render(request, 'tutors/schedule.html', context)

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
    return render(request, 'tutors/sis_search.html', results_dict)

def add_course(request, course_id):
    tutor = request.user.profile.tutor
    course = get_object_or_404(Course, id=course_id)
    courses = tutor.courses.all()
    if course not in courses:
        tutor.courses.add(course)
    tutor.save()
    return render(request, 'tutors/sis_search.html')

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
        print(c['subject'], c['catalog_nbr'], c['instructors'], c['crse_id'], c['descr'])
    return r.json()

def update_profile(request):
    tutor = request.user.profile.tutor
    tutor.profile.first_name = request.GET.get('first_name')
    tutor.profile.last_name = request.GET.get('last_name')
    tutor.pay_rate = request.GET.get('pay_rate')
    tutor.about_me = request.GET.get('about_me')
    tutor.save()
    return render(request, 'tutors/index.html')

def accept_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    request_obj.accepted = True
    request_obj.save()
    return session(request, request_id)

def reject_request(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    request_obj.rejected = True
    request_obj.save()
    return show_requests(request)

def session(request, request_id):
    context = {
        'request': request_id,
    }
    return render(request, 'tutors/session.html', context)

def make_session(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    day = request.POST.get('session-date')
    print('DAY:', request.POST.get('session-date'))
    print('START:', request.POST.get('session-start-time'))
    print('END:', request.POST.get('session-end-time'))
    print('STUDENT', request_obj.student)
    start_time = datetime.strptime(f"{day} {request.POST.get('session-start-time')}", '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(f"{day} {request.POST.get('session-end-time')}", '%Y-%m-%d %H:%M')
    session = Session(tutor=request_obj.tutor, student=request_obj.student, start_time=start_time, end_time=end_time, course=request_obj.course)
    session.save()
    return show_requests(request)