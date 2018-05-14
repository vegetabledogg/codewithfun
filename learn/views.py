from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from learn.forms import SubmissionForm
from accounts.models import User
from learn.models import Lesson, Submission, Course, HaveLearned, Category, TriedCourse
from learn.tasks import evaluate_submission
from django.http import JsonResponse
def learn(request, category_url=None):
    if category_url:
        category = Category.objects.get(category_slug=category_url)
        courses = Course.objects.filter(category=category)
    else:
        courses = Course.objects.all()
    return render(request, 'learn/learn.html', {'all_courses': courses})

def course_detail(request, course_url):
    course = Course.objects.get(course_slug=course_url)
    lessons = Lesson.objects.filter(course=course).order_by('lesson_num')
    proportion = 0
    current_user = request.user
    all_learned_courses = []
    current_lesson = None
    if request.user.is_authenticated():
        tried_courses = TriedCourse.objects.filter(user=current_user)
        for each_leasson in tried_courses:
            all_learned_courses.append(each_leasson.course) 
        count = 0
        for lesson in lessons:
            count += len(HaveLearned.objects.filter(user=current_user, lesson=lesson))
        total_lesson = course.total_lesson()
        
            
        if total_lesson != 0:
            proportion = count / total_lesson
            current_lesson = Lesson.objects.get(lesson_num=count)
        if request.method == 'POST':
            TriedCourse.objects.get_or_create(user=current_user, course=course)
        
    return render(request, 'learn/course_detail.html', {'course': course, "lessons": lessons, "proportion": proportion, 'all_learned_courses': all_learned_courses, 'current_lesson':current_lesson})

@login_required
def lesson(request, course_url, lesson_url):
    lesson = Lesson.objects.get(lesson_slug=lesson_url)
    try:
        next_lesson = Lesson.objects.get(course=lesson.course, lesson_num=int(lesson.lesson_num)+1)
    except:
        next_lesson = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission(code=form.cleaned_data['code'], lesson=lesson, submitter=request.user)
            submission.save()
            evaluate_submission(submission, lesson)
            data = {'status': submission.status, 'result': submission.result, 'next_lesson': next_lesson}
            if submission.status == 'AC':
                HaveLearned.objects.get_or_create(user=submission.submitter, lesson=lesson)
            
            # return render(request, 'learn/lesson.html', {'course_url': course_url, 'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'sub': submission})              
            return JsonResponse(data)
    else:
        form = SubmissionForm(initial={'code': lesson.precode}) # 表单初始时在代码编辑区会显示预设代码
    return render(request, 'learn/lesson.html', {'course_url': course_url, 'lesson': lesson, 'next_lesson': next_lesson, 'form': form})
