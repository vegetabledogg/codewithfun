from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Course, Lesson, ToLearn

def learn(request):
    all_courses = Course.objects.all()
    return render(request, 'learn/learn.html', {'all_courses': all_courses})

def course_detail(request, pk):
    course = Course.objects.get(course_name=pk) #get_object_or_404(Course)
    all_lessons = Lesson.objects.filter(course=course)
    proportion = ToLearn.objects.get(course=course).lesson_num / course.total_lesson
    return render(request, 'learn/course_detail.html',{'course': course, "all_lessons": all_lessons, "proportion": proportion})

@login_required
def course1(request):
    return render(request, 'learn/course_base.html')