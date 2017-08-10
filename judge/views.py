from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from judge.forms import SubmissionForm
from accounts.models import Profile
from judge.models import Lesson, Submission
from judge.task import evaluate_submission

def learn(request):
    return render(request, 'learn/learn.html')

@login_required
def course1(request):
    return render(request, 'learn/course_base.html')

@login_required
def lesson(request, lid):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            submission.lesson = Lesson.objects.get(pk=lid)
            submission.submitter = Profile.objects.get(user=request.user)
            submission.save()
            evaluate_submission.delay(submission.id)
            return render()
    else:
        form = SubmissionForm()
        return render()

