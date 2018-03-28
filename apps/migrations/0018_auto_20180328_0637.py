# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0017_easyinstruction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competequiz',
            name='category',
        ),
        migrations.DeleteModel(
            name='EasyInstruction',
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
            name='Quiz',
        ),
    ]
