# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tolearn',
            name='course',
        ),
        migrations.RemoveField(
            model_name='tolearn',
            name='user',
        ),
        migrations.AddField(
            model_name='havelearned',
            name='lesson',
            field=models.ForeignKey(default='', to='judge.Lesson'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ToLearn',
        ),
    ]
