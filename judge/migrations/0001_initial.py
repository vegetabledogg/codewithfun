# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import judge.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('course_name', models.CharField(max_length=255)),
                ('brief', models.TextField()),
                ('overview', models.TextField()),
                ('classification', models.CharField(max_length=32)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('course_auth', models.CharField(max_length=255, default='admin')),
                ('total_lesson', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HaveLearned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('course', models.ForeignKey(to='judge.Course')),
                ('user', models.ForeignKey(to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('lesson_name', models.CharField(max_length=255)),
                ('lesson_num', models.IntegerField()),
                ('learn', models.TextField()),
                ('instructions', models.TextField()),
                ('hint', models.TextField()),
                ('language', models.CharField(max_length=32)),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.CharField(max_length=16)),
                ('course', models.ForeignKey(to='judge.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('code', models.TextField()),
                ('status', models.CharField(max_length=8, default='AC')),
                ('result', models.TextField(default='')),
                ('lesson', models.ForeignKey(to='judge.Lesson')),
                ('submitter', models.ForeignKey(to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('inputfile', models.FileField(upload_to=judge.models.in_upload_path)),
                ('outputfile', models.FileField(upload_to=judge.models.out_upload_path)),
                ('lesson', models.ForeignKey(to='judge.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='ToLearn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('lesson_num', models.IntegerField()),
                ('course', models.ForeignKey(to='judge.Course')),
                ('user', models.ForeignKey(to='accounts.Profile')),
            ],
        ),
    ]
