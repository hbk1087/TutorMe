from django.contrib import admin
from .models import Profile, Tutor, Student, Request, Course, Session
# Register your models here.
admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Request)
admin.site.register(Course)
admin.site.register(Session)
