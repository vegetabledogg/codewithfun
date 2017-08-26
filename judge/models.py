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
    classification = models.CharField(max_length=32)
    release_date = models.DateTimeField(auto_now_add=True)
    course_auth = models.CharField(max_length=255, default='admin')

    def __str__(self):
        return self.course_name
    
    def total_lesson(self):
        return self.lesson_set.all().count()


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
    submitter = models.ForeignKey('accounts.User')
    code = models.TextField()
    status = models.CharField(max_length=8, default='')
    result = models.TextField(default='')

class HaveLearned(models.Model):
    user = models.ForeignKey('accounts.User')
    lesson = models.ForeignKey(Lesson)
