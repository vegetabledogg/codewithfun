from django.contrib import admin
from . models import Course, Lesson, ToLearn

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(ToLearn)