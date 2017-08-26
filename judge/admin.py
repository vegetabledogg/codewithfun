from django.contrib import admin
from judge.models import Course, Lesson, Testcase, HaveLearned

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ['course_name']

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    fieldsets = [
        (None, {'fields': ['course']}),
        ('Content', {'fields': ['lesson_name', 'lesson_num', 'learn', 'instructions', 'hint']}),
        ('Constraints', {'fields': ['language', 'time_limit', 'memory_limit']})
    ]
    list_display = ['course', 'lesson_name','lesson_num']
    actions = ['delete_selected']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Testcase)
