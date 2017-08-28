from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField

def in_upload_path(instance, filename):
    """ Function to return upload path for test case input file"""
    return "/".join(["testcases", str(instance.lesson.id)]) + ".in"


def out_upload_path(instance, filename):
    """ Function to return upload path for test case output file"""
    return "/".join(["testcases", str(instance.lesson.id)]) + ".out"

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    brief = RichTextField()
    overview = RichTextField()
    classification = models.CharField(max_length=32) # 课程所属分类
    release_date = models.DateTimeField(auto_now_add=True)
    course_auth = models.CharField(max_length=255, default='admin')

    def __str__(self):
        return self.course_name
    
    def total_lesson(self):
        return self.lesson_set.all().count()

    def get_course_url(self):
        self.course_url = self.course_name.replace(' ', '$')


class Lesson(models.Model): 
    LANGUAGE_IN_LESSON_CHOICES = (
        ('Python', 'Python'),
        ('C', 'C'),
        ('C++', 'C++')
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=255)
    lesson_num = models.IntegerField()
    learn = RichTextField()
    instructions = RichTextField()
    hint = RichTextField()
    language = models.CharField(max_length=32, choices=LANGUAGE_IN_LESSON_CHOICES, default='C')
    time_limit = models.CharField(max_length=16) # 解题代码时间限制
    memory_limit = models.CharField(max_length=16) # 解题代码内存限制
    precode = RichTextField() # 代码编辑区预设代码

    def __str__(self):
        return str(self.lesson_name)

    def get_lesson_url(self):
        self.lesson_url = self.lesson_name.replace(' ', '$')

class Testcase(models.Model):
    lesson = models.ForeignKey(Lesson)
    inputfile = models.FileField(upload_to=in_upload_path)
    outputfile = models.FileField(upload_to=out_upload_path)

class Submission(models.Model):
    lesson = models.ForeignKey(Lesson)
    submission_time = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey('accounts.User')
    code = models.TextField()
    status = models.CharField(max_length=8, default='') # 判题结果
    result = models.TextField(default='') # 代码执行后的标准输出和标准错误

class HaveLearned(models.Model):
    user = models.ForeignKey('accounts.User')
    lesson = models.ForeignKey(Lesson)
