from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import User
from judge.models import Lesson, Submission, Course, HaveLearned
from judge.tasks import evaluate_submission

def learn(request):
    courses = Course.objects.all()
    for course in courses:
        course.get_course_url()
    return render(request, 'learn/learn.html', {'all_courses': courses})

def course_detail(request, course_url):
    course_name = course_url.replace('$', ' ')
    course = Course.objects.get(course_name=course_name)
    lessons = Lesson.objects.filter(course=course)
    proportion = 0
    current_user = request.user
    if request.user.is_authenticated():
        count = 0
        for lesson in lessons:
            count += len(HaveLearned.objects.filter(user=current_user, lesson=lesson))
            lesson.get_lesson_url()
        total_lesson = course.total_lesson()
        if total_lesson != 0:
            proportion = count / total_lesson
    else:
        for lesson in lessons:
            lesson.get_lesson_url()         
    course.get_course_url()
    return render(request, 'learn/course_detail.html',{'course': course, "lessons_with_url": lessons, "proportion": proportion})

@login_required
def lesson(request, course_url, lesson_url, lesson_num):
    lesson_name = lesson_url.replace('$', ' ')
    lesson = Lesson.objects.get(lesson_name=lesson_name, lesson_num=int(lesson_num))
    try:
        next_lesson = Lesson.objects.get(course=lesson.course, lesson_num=int(lesson.lesson_num)+1)
        next_lesson.get_lesson_url()
    except:
        next_lesson = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission(code=form.cleaned_data['code'], lesson=lesson, submitter=request.user)
            #submission.save()
            #evaluate_submission(submission.id)
            evaluate_submission(submission, lesson)
            #sub = Submission.objects.get(pk=submission.id)
            if submission.status == 'AC':
                HaveLearned.objects.get_or_create(user=submission.submitter, lesson=lesson)
            return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'sub': submission, 'course_url': course_url})              
    else:
        form = SubmissionForm(initial={'code': lesson.precode}) # 表单初始时在代码编辑区会显示预设代码
    return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'course_url': course_url})
