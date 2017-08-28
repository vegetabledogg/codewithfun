from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.models import User
from judge.models import Lesson, Submission, Course, HaveLearned
from accounts.forms import SignUpForm, EditForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

@login_required
def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user) #加入修改后的信息
        if form.is_valid():
            form.save()
            return redirect('learn')
    else:
        form = EditForm(instance=request.user) #加载原始信息
    return render(request, 'edit.html', {'form': form})

@login_required
def change_pwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('learn')  
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pwd.html', {'form': form})

@login_required
def learned_course(request):
    current_user = User.objects.get(id=request.user.id)
    all_learned_lessons = HaveLearned.objects.filter(user=current_user)
    all_learned_courses = []
    for each_leasson in all_learned_lessons:
        if each_leasson.lesson.course not in all_learned_courses:
            course = each_leasson.lesson.course
            course.get_course_url()
            all_learned_courses.append(course)
    return render(request, 'learned_course.html', {'all_learned_courses': all_learned_courses})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('learn')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
