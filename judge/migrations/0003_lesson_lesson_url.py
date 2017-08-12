# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_course_course_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_url',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
