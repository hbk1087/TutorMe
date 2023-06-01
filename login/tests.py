from django.test import TestCase
from students.views import url_creator
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.test import Client
from django.test.utils import setup_test_environment
from login.models import Student, Profile, Request, Tutor


class TestUtils(TestCase):
    def test_create_url(self):
        url = url_creator('23', 'spring', 'Cs', '3240', 'horton')
        print(url)
        self.assertEqual(url, 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=CS&catalog_nbr=3240&instructor_name=horton')

class ProfileInitialTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test')
        self.user.save()
        self.prof = Profile(user=self.user, first_name = 'test', last_name='dummy')
    
    def test_profile_first_name(self):
        self.assertEquals(self.prof.first_name, 'test')

    def test_profile_last_name(self):
        self.assertEquals(self.prof.last_name, 'dummy')

    def test_profile_default_student(self):
        self.assertEquals(self.prof.is_student, True)

    def test_profile_default_exists(self):
        self.assertEquals(self.prof.exists, True)

    def test_profile_user_object(self):
        self.assertEquals(self.user.username, 'test')

class StudentInitialTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test', id='1')
        self.user.save()
        self.prof = Profile(user=self.user, first_name = 'test', last_name='dummy')
        self.stu = Student(profile=self.prof)

    def test_student_first_name(self):
        self.assertEquals(self.prof.first_name, 'test')

    def test_student_last_name(self):
        self.assertEquals(self.prof.last_name, 'dummy')

    def test_student_default_student(self):
        self.assertEquals(self.prof.is_student, True)

    def test_student_default_exists(self):
        self.assertEquals(self.prof.exists, True)

    def test_student_user_object(self):
        self.assertEquals(self.user.username, 'test')

    def test_student_profile_object(self):
        self.assertEquals(self.stu.profile, self.prof)

class TutorInitialTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test', id='1')
        self.user.save()
        self.prof = Profile(user=self.user, first_name = 'test', last_name='dummy')
        self.stu = Tutor(profile=self.prof)

    def test_student_first_name(self):
        self.assertEquals(self.prof.first_name, 'test')

    def test_tutor_last_name(self):
        self.assertEquals(self.prof.last_name, 'dummy')

    # def test_tutor_default_student(self):
    #     self.assertEquals(self.prof.is_student, False)

    def test_tutor_default_exists(self):
        self.assertEquals(self.prof.exists, True)

    def test_tutor_user_object(self):
        self.assertEquals(self.user.username, 'test')

    def test_tutor_profile_object(self):
        self.assertEquals(self.stu.profile, self.prof)


class RequestInitialTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test', id='1')
        self.user.save()
        self.prof = Profile(user=self.user, first_name = 'student', last_name='dummy')
        self.stu = Student(profile=self.prof)
        self.prof2 = Profile(user=self.user, first_name = 'student', last_name='dummy')
        self.tut = Tutor(profile=self.prof2)

        self.req = Request(tutor=self.tut, student=self.stu)

    def request_student_test(self):
        self.assertEquals(self.req.student, self.stu)

    def request_tutor_test(self):
        self.assertEquals(self.req.tutor, self.tut)

    def request_accepted_test(self):
        self.assertEquals(self.req.accepted, False)

    def request_rejected_test(self):
        self.assertEquals(self.req.rejected, False)