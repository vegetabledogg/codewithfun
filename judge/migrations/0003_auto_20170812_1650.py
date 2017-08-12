# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_auto_20170811_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='time_limit',
            field=models.CharField(max_length=16),
        ),
    ]
