# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0019_auto_20180328_0638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='easy_instr',
        ),
        migrations.RemoveField(
            model_name='competequiz',
            name='category',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='CompeteQuiz',
        ),
        migrations.DeleteModel(
            name='EasyInstruction',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
