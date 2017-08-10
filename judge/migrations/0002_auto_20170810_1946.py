# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import judge.models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('inputfile', models.FileField(upload_to=judge.models.in_upload_path)),
                ('outputfile', models.FileField(upload_to=judge.models.out_upload_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='inputfile',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='outputfile',
        ),
        migrations.AddField(
            model_name='lesson',
            name='language',
            field=models.CharField(max_length=255, default=''),
        ),
        migrations.AddField(
            model_name='lesson',
            name='memory_limit',
            field=models.IntegerField(default=65536),
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_limit',
            field=models.IntegerField(default=400),
        ),
        migrations.AddField(
            model_name='testcase',
            name='lesson',
            field=models.ForeignKey(to='judge.Lesson'),
        ),
    ]
