from django.db import models
from accounts.models import Profile
import copy

def in_upload_path(instance, filename):
    """ Function to return upload path for test case input file"""
    return "/".join(["testcases", str(instance.lesson.id)]) + ".in"


def out_upload_path(instance, filename):
    """ Function to return upload path for test case output file"""
    return "/".join(["testcases", str(instance.lesson.id)]) + ".out"

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    brief = models.TextField()
    overview = models.TextField()
    classification = models.CharField(max_length=32)
    release_date = models.DateTimeField(auto_now_add=True)
    course_auth = models.CharField(max_length=255, default='admin')
    total_lesson = models.IntegerField(default=0)
    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=255)
    lesson_num = models.IntegerField()
    learn = models.TextField()
    instructions = models.TextField()
    hint = models.TextField()
    language = models.CharField(max_length=32)
    time_limit = models.CharField(max_length=16)
    memory_limit = models.CharField(max_length=16)
    def __str__(self):
        return str(self.lesson_name)

class Testcase(models.Model):
    lesson = models.ForeignKey(Lesson)
    inputfile = models.FileField(upload_to=in_upload_path)
    outputfile = models.FileField(upload_to=out_upload_path)

class Submission(models.Model):
    lesson = models.ForeignKey(Lesson)
    submission_time = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey('accounts.Profile')
    code = models.TextField()
    status = models.CharField(max_length=8, default='')
    result = models.TextField(default='')

class HaveLearned(models.Model):
    user = models.ForeignKey('accounts.Profile')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
