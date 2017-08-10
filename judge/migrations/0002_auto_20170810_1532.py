# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import judge.models
import datetime
from django.utils.timezone import utc


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
            field=models.CharField(max_length=16, default=datetime.datetime(2017, 8, 10, 7, 31, 50, 475440, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='memory_limit',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='time_limit',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='result',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(max_length=8, default='AC'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='lesson',
            field=models.ForeignKey(to='judge.Lesson'),
        ),
    ]
