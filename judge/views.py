from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import Profile
from judge.models import Lesson, Submission, ToLearn, Course
from judge.tasks import evaluate_submission

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
def lesson(request, course_url, lesson_url, lesson_num):
    lesson = Lesson.objects.get(lesson_url=lesson_url, lesson_num=lesson_num)
    try:
        next_lesson = Lesson.objects.get(course=lesson.course, lesson_num=lesson.lesson_num+1)
    except:
        next_lesson = lesson
        next_lesson.lesson_num += 1
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission()
            submission.code = form.cleaned_data['code']
            submission.lesson = Lesson.objects.get(pk=lesson.id)
            submission.submitter = Profile.objects.get(user=request.user)
            submission.save()
            # evaluate_submission.delay(submission.id)
            # print(submission.id)
            evaluate_submission(submission.id)
            sub = Submission.objects.get(pk=submission.id)
            # print(sub.id)
            # print(sub.status)
            # print(sub.result)
            return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'sub': sub, 'course_url': course_url})
    else:
        form = SubmissionForm()
<<<<<<< HEAD
        return render(request, 'learn/lesson.html', {'lesson': lesson, 'form': form})
=======
        return render(request, 'learn/lesson.html', {'lesson': lesson, 'next_lesson': next_lesson, 'form': form, 'course_url': course_url})

>>>>>>> 8af95fa3cb810391a7e7a1bc873fb938739a3300
