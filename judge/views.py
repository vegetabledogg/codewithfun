from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def learn(request):
    return render(request, 'learn/learn.html')

@login_required
def course1(request):
    return render(request, 'learn/course_base.html')