from django.contrib import admin
from .models import Course
from .models import StudentProfile

admin.site.register(StudentProfile)
admin.site.register(Course)
