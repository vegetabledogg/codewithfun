from django.contrib import admin
from judge.models import Course, Lesson, ToLearn, Testcase

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(ToLearn)
admin.site.register(Testcase)
