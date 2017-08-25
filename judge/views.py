from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import User
from judge.models import Lesson, Submission, Course, HaveLearned
from judge.tasks import evaluate_submission

'''class CourseWithUrl:
    def __init__(self, course):
        self.course_name = course.course_name
        self.brief = course.brief
        self.classification = course.classification
        self.overview = course.overview
        self.course_auth = course.course_auth
        self.release_date = course.release_date
        self.total_lesson = course.total_lesson
        self.course_url = course.course_name.replace(' ', '$')

class LessonWithUrl:
    def __init__(self, lesson):
        self.lesson_name = lesson.lesson_name
        self.lesson_num = lesson.lesson_num
        self.learn = lesson.learn
        self.instructions = lesson.instructions
        self.hint = lesson.hint
        self.language = lesson.language
        self.memory_limit = lesson.memory_limit
        self.time_limit = lesson.time_limit
        self.lesson_url = lesson.lesson_name.replace(' ', '$')'''

def learn(request):
    courses = Course.objects.all()
    for course in courses:
        course.course_url = course.course_name.replace(' ', '$')
    return render(request, 'learn/learn.html', {'all_courses': courses})

def course_detail(request, course_url):
    course_name = course_url.replace('$', ' ')
    if request.user.is_authenticated():
        current_user = request.user
    else:
        current_user = None
    course = Course.objects.get(course_name=course_name)
    lessons = Lesson.objects.filter(course=course)
    count = 0
    for lesson in lessons:
        if current_user:
            count += len(HaveLearned.objects.filter(user=current_user, lesson=lesson))
        lesson.lesson_url = lesson.lesson_name.replace(' ', '$')
    if course.total_lesson != 0:
        proportion = count / course.total_lesson
    else:
        proportion = 0
    course.course_url = course.course_name.replace(' ', '$')
    return render(request, 'learn/course_detail.html',{'course': course, "lessons_with_url": lessons, "proportion": proportion})

@login_required
def lesson(request, course_url, lesson_url, lesson_num):
    lesson_name = lesson_url.replace('$', ' ')
    lesson = Lesson.objects.get(lesson_name=lesson_name, lesson_num=int(lesson_num))
    try:
        next_lesson = Lesson.objects.get(course=lesson.course, lesson_num=int(lesson.lesson_num)+1)
        next_lesson.lesson_url = next_lesson.lesson_name.replace(' ', '$')
    except:
        next_lesson = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.code = form.cleaned_data['code']
            submission.lesson = Lesson.objects.get(pk=lesson.id)
            submission.submitter = request.user
            submission.save()
            evaluate_submission(submission.id)
            sub = Submission.objects.get(pk=submission.id)
            if sub.status == 'AC':
                havelearned = HaveLearned()
                havelearned.lesson = lesson
                havelearned.user = submission.submitter
                havelearned.save()
            return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'sub': sub, 'course_url': course_url})              
    else:
        form = SubmissionForm()
    return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'course_url': course_url})


