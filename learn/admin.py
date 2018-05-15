from django.contrib import admin
from learn.models import Course, Lesson, Testcase, HaveLearned, Category

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ['course_name']

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    fieldsets = [
        (None, {'fields': ['course']}),
        ('Content', {'fields': ['lesson_name', 'lesson_num', 'learn', 'instructions', 'hint', 'precode']}),
        ('Constraints', {'fields': ['language', 'time_limit', 'memory_limit']})
    ]
    list_display = ['course', 'lesson_name','lesson_num']
    actions = ['delete_selected']

class CategoryAdmin(admin.ModelAdmin):
    model = Category

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Testcase)
admin.site.register(Category, CategoryAdmin)
