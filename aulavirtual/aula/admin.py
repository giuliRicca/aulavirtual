from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Classroom, Student, Subject,
                     Assignment, Response, Notification])
