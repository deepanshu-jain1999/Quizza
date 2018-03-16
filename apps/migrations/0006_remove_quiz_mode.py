# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_quiz_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='mode',
        ),
    ]
