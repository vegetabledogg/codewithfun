from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from accounts.models import User
from learn.models import Lesson, Submission, Course, HaveLearned, TriedCourse
from accounts.forms import EditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
import re

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
    tried_courses = TriedCourse.objects.filter(user=current_user)
    all_learned_courses = []
    learned_course_num = 0
    for each_leasson in tried_courses:
        all_learned_courses.append(each_leasson.course) 
    learned_course_num = len(all_learned_courses)
    return render(request, 'learned_course.html', {'all_learned_courses': all_learned_courses,'learned_course_num': learned_course_num})

def my_validate_email(email):  
    from django.core.validators import validate_email  
    from django.core.exceptions import ValidationError  
    try:  
        validate_email(email)  
        return True  
    except ValidationError:  
        return False

username_pattern = re.compile(r'^[\w\.\+\-@]+$')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password_1 = request.POST['password1']
        raw_password_2 = request.POST['password2']
        email = request.POST['email']
        if re.match(username_pattern, username) is None:
            json_response = {'status': 'error', 'field': 'username', 'error_message': '用户名格式错误'}
        elif User.objects.filter(username=username).count() > 0:
            json_response = {'status': 'error', 'field': 'username', 'error_message': '用户名已经被占用'}
        elif len(raw_password_1) < 6:
            json_response = {'status': 'error', 'field': 'password1', 'error_message': '密码少于6位'}
        elif len(raw_password_2) < 6:
            json_response = {'status': 'error', 'field': 'password2', 'error_message': '密码少于6位'}
        elif raw_password_1 != raw_password_2:
            json_response = {'status': 'error', 'field': 'password2', 'error_message': '两次密码不一致'}
        elif my_validate_email(email) == False:
            json_response = {'status': 'error', 'field': 'email', 'error_message': '邮箱格式错误'}
        else:
            user = User.objects.create_user(username, email, raw_password_1)             
            user = authenticate(username=username, password=raw_password_1)
            login(request, user)
            json_response = {'status': 'success'}
        return JsonResponse(json_response)
    else:
        return render(request, 'signup.html') 

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            json_response = {'status': 'success'}
            login(request, user)
        else:
            json_response = {'status': 'error','field': 'password', 'error_message': '密码错误'}
        return JsonResponse(json_response)
    else:
        return render(request, 'login.html')

def my_logout(request):
    logout(request)
    return redirect('learn')
