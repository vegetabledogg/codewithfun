from django.contrib import admin
from learn.models import Course, Lesson, Testcase, HaveLearned, Category

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ['course_name']
    prepopulated_fields = {'course_slug': ('course_name',)}

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    fieldsets = [
        (None, {'fields': ['course']}),
        ('Content', {'fields': ['lesson_name', 'lesson_num', 'lesson_slug', 'learn', 'instructions', 'hint', 'precode']}),
        ('Constraints', {'fields': ['language', 'time_limit', 'memory_limit']})
    ]
    list_display = ['course', 'lesson_name','lesson_num']
    actions = ['delete_selected']
    prepopulated_fields = {'lesson_slug': ('lesson_name', 'lesson_num')}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Testcase)
admin.site.register(Category, CategoryAdmin)
