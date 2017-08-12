from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import Profile
from judge.models import Lesson, Submission, ToLearn, Course
from judge.task import evaluate_submission

def learn(request):
    all_courses = Course.objects.all()
    return render(request, 'learn/learn.html', {'all_courses': all_courses})

def course_detail(request, course_url):
    course = Course.objects.get(course_url=course_url)
    all_lessons = Lesson.objects.filter(course=course)
    set_user = ToLearn.objects.filter(course=course)
    current_user = Profile.objects.get(user=request.user)
    proportion = set_user.get(user=current_user).lesson_num / course.total_lesson
    return render(request, 'learn/course_detail.html',{'course': course, "all_lessons": all_lessons, "proportion": proportion})

'''
@login_required
def course1(request):
    return render(request, 'learn/course_base.html')
'''
@login_required
def lesson(request, lid):
    lesson = Lesson.objects.get(pk=lid)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            submission.lesson = lesson
            submission.submitter = Profile.objects.get(user=request.user)
            submission.save()
            evaluate_submission.delay(submission.id)
            return render(request, 'learn/lesson.html', {'lesson': lesson, 'form': form})
    else:
        form = SubmissionForm()
        return render(request, 'learn/lesson.html', {'lesson': lesson, 'form': form})