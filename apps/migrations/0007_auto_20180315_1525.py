# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_remove_quiz_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(to='apps.Category'),
        ),
    ]
