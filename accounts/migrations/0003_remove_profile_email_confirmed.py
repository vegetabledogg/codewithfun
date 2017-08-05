# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170805_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email_confirmed',
        ),
    ]
