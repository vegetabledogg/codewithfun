# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_url',
            field=models.CharField(max_length=255, default='pythonlesson'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(max_length=8, default=''),
        ),
    ]
