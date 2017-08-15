from codewithfun.forms import LessonForm
from judge.models import Lesson
from django.shortcuts import render, redirect

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = Lesson()
            lesson.course = form.cleaned_data['course']
            lesson.lesson_name = form.cleaned_data['lesson_name']
            lesson.lesson_num = form.cleaned_data['lesson_num']
            lesson.learn = form.cleaned_data['learn']
            lesson.instructions = form.cleaned_data['instructions']
            lesson.hint = form.cleaned_data['hint']
            lesson.language = form.cleaned_data['language']
            lesson.time_limit = form.cleaned_data['time_limit']
            lesson.memory_limit = form.cleaned_data['memory_limit']
            lesson.course.total_lesson += 1
            lesson.save()
            return redirect('/admin/')
    else:
        form = LessonForm()
    return render(request, 'admin/add_lesson.html', {'form': form})
