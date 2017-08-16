from .forms import LessonForm
from judge.models import Lesson, Course
from django.shortcuts import render, redirect, get_object_or_404

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
            lesson.course.save()
            lesson.save()
            return redirect('/admin/')
    else:
        form = LessonForm()
    return render(request, 'admin/add_lesson.html', {'form': form})

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.course.total_lesson -= 1
    lesson.course.save()
    lesson.delete()
    return redirect('/admin/')
