from django.contrib import admin
from judge.models import Course, Lesson, ToLearn, Testcase

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ['course_name']

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ['course', 'lesson_name','lesson_num']

class ToLearnAdmin(admin.ModelAdmin):
    model = ToLearn
    list_display = ['user', 'course', 'lesson_num']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ToLearn, ToLearnAdmin)
admin.site.register(Testcase)

