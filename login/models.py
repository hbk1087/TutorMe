from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField

def default_crse_ids():
    return ['404']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    #student_major = models.CharField(max_length=30, blank=True)
    is_student = models.BooleanField(default=True)
    exists = models.BooleanField(default=True)
    # Add any other fields you want to add here
    def __str__(self) -> str:
        return "Profile: " + self.user.first_name + " " + self.user.last_name


class Student(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    tutors = models.ManyToManyField('Tutor', related_name='tutors')
    requests = models.ManyToManyField('Request', related_name='requests_by_student')
    about_me = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return "Student: " + self.profile.first_name + " " + self.profile.last_name

# class Day(models.Model):
#     DAY_CHOICES = (
#         ('Mon', 'Monday'),
#         ('Tue', 'Tuesday'),
#         ('Wed', 'Wednesday'),
#         ('Thu', 'Thursday'),
#         ('Fri', 'Friday'),
#         ('Sat', 'Saturday'),
#         ('Sun', 'Sunday'),
#     )
#     day = models.CharField(max_length=3, choices=DAY_CHOICES)


class Tutor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    pay_rate = models.IntegerField()
    courses = models.ManyToManyField('Course', related_name='tutors')
    students = models.ManyToManyField('Student', related_name='students')
    requests = models.ManyToManyField('Request', related_name='requests_for_tutor')
    about_me = models.CharField(max_length=200, blank=True)
    # days = models.ManyToManyField('Day', through='Availability')

    # def get_available_days(self):
    #     available_days = []
    #     for schedule in self.schedules.all():
    #         if schedule.is_available:
    #             available_days.append(schedule.day_of_week)
    #     return available_days

    def __str__(self) -> str:
        return "Tutor: " + self.profile.first_name + " " + self.profile.last_name
    
# class Availability(models.Model):
#     tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
#     day = models.ForeignKey(Day, on_delete=models.CASCADE)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

class Request(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.student.profile.first_name + " requests " + self.tutor.profile.first_name + " for " + self.course.subject + " " + self.course.catalog_nbr
    
class Course(models.Model):
    crse_id = models.CharField(max_length=6)
    subject = models.CharField(max_length=6)
    catalog_nbr = models.CharField(max_length=4)

    def __str__(self) -> str:
        return self.subject + " " + self.catalog_nbr
    
class Session(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} session with {self.tutor.profile.first_name} and {self.student.profile.first_name}"