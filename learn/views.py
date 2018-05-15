from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from learn.forms import SubmissionForm
from accounts.models import User
from learn.models import Lesson, Submission, Course, HaveLearned, Category, TriedCourse
from learn.tasks import evaluate_submission
from django.http import JsonResponse, HttpResponseNotFound

def learn(request):
    if 'category-id' in request.GET.keys():
        category = get_object_or_404(Category, pk=request.GET['category-id'])
        courses = Course.objects.filter(category=category)
    else:
        courses = Course.objects.all()
    return render(request, 'learn/learn.html', {'courses': courses})

def course_detail(request):
    if 'course-id' in request.GET.keys():
        course = get_object_or_404(Course, pk=request.GET['course-id'])
    else:
        return HttpResponseNotFound()
    lessons = Lesson.objects.filter(course=course).order_by('lesson_num')
    all_learned_courses = []
    current_lesson = None
    proportion = 0
    if request.user.is_authenticated():
        tried_courses = TriedCourse.objects.filter(user=request.user)
        all_learned_courses = [tried_course.course for tried_course in tried_courses] 
        total_lesson = course.total_lesson()
        if total_lesson != 0:
            max_lesson_num = 0
            count = 0
            for lesson in lessons:
                try:
                    HaveLearned.objects.get(user=request.user, lesson=lesson)
                    if max_lesson_num < lesson.lesson_num:
                        max_lesson_num = lesson.lesson_num
                    count += 1
                except:
                    continue
            if max_lesson_num != total_lesson:
                max_lesson_num += 1
            current_lesson = Lesson.objects.get(course=course, lesson_num=max_lesson_num)
            proportion = count / total_lesson
        if request.method == 'POST':
            TriedCourse.objects.get_or_create(user=request.user, course=course)       
    return render(request, 'learn/course_detail.html', {'course': course, "lessons": lessons, 'all_learned_courses': all_learned_courses, 'current_lesson':current_lesson, 'proportion': proportion})

@login_required
def lesson(request):
    if 'lesson-id' in request.GET.keys():
        lesson = get_object_or_404(Lesson, pk=request.GET['lesson-id'])
    else:
        return HttpResponseNotFound()
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
            return JsonResponse(data)
    else:
        form = SubmissionForm(initial={'code': lesson.precode}) # 表单初始时在代码编辑区会显示预设代码
    return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form})
