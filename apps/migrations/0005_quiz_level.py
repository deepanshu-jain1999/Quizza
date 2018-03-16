# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_auto_20180314_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='level',
            field=models.CharField(max_length=20, default='NONE', choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')]),
        ),
    ]
