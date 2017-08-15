from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import Profile
from judge.models import Lesson, Submission, Course, HaveLearned
from judge.tasks import evaluate_submission
from .admin import LessonAdmin
import copy

class CourseWithUrl(Course):
    def __init__(self, course):
        self.course_name = course.course_name
        self.brief = course.brief
        self.classification = course.classification
        self.overview = course.overview
        self.course_auth = course.course_auth
        self.release_date = course.release_date
        self.total_lesson = course.total_lesson
        self.course_url = course.course_name.replace(' ', '$')

class LessonWithUrl(Lesson):
    def __init__(self, lesson):
        self.lesson_name = lesson.lesson_name
        self.lesson_num = lesson.lesson_num
        self.learn = lesson.learn
        self.instructions = lesson.instructions
        self.hint = lesson.hint
        self.language = lesson.language
        self.memory_limit = lesson.memory_limit
        self.time_limit = lesson.time_limit
        self.lesson_url = lesson.lesson_name.replace(' ', '$')

def learn(request):
    courses = Course.objects.all()
    all_courses = []
    for course in courses:
        all_courses.append(CourseWithUrl(course))
    return render(request, 'learn/learn.html', {'all_courses': all_courses})

def course_detail(request, course_url):
    course_name = course_url.replace('$', ' ')
    course = Course.objects.get(course_name=course_name)
    lessons = Lesson.objects.filter(course=course)
    all_lessons = []
    for lesson in lessons:
        all_lessons.append(LessonWithUrl(lesson))
    set_user = HaveLearned.objects.filter(course=course)
    current_user = Profile.objects.filter(user=request.user)
    proportion = set_user.filter(user=current_user).count() / course.total_lesson
    course = CourseWithUrl(course)
    return render(request, 'learn/course_detail.html',{'course': course, "all_lessons": all_lessons, "proportion": proportion})

@login_required
def lesson(request, course_url, lesson_url, lesson_num):
    lesson_name = lesson_url.replace('$', ' ')
    lesson = Lesson.objects.get(lesson_name=lesson_name, lesson_num=lesson_num)
    next_lesson = Lesson.objects.filter(course=lesson.course, lesson_num=lesson.lesson_num+1)
    if len(next_lesson) > 0:
        next_lesson = LessonWithUrl(next_lesson[0])
    else:
        next_lesson = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.code = form.cleaned_data['code']
            submission.lesson = Lesson.objects.get(pk=lesson.id)
            submission.submitter = Profile.objects.get(user=request.user)
            submission.save()
            evaluate_submission(submission.id)
            sub = Submission.objects.get(pk=submission.id)
            if sub.status == 'AC':
                havelearned = HaveLearned()
                havelearned.course = lesson.course
                havelearned.lesson = lesson
                havelearned.user = request.user
                havelearned.save()
            return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'sub': sub, 'course_url': course_url})              
    else:
        form = SubmissionForm()
    return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'course_url': course_url})
'''
def add_lesson(request):
    if request.method == 'POST':
        form = LessonAdmin(request.POST)
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
            return ()
    else:
        form = LessonAdmin()
        return '''
