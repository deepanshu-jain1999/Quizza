# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0015_auto_20180323_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='time_per_ques_easy',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='category',
            name='time_per_ques_hard',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='category',
            name='time_per_ques_medium',
            field=models.IntegerField(default=40),
        ),
    ]
