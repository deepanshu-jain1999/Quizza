# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0027_auto_20180409_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='score',
            new_name='all_score',
        ),
        migrations.AddField(
            model_name='score',
            name='easy_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='score',
            name='hard_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='score',
            name='medium_score',
            field=models.FloatField(default=0.0),
        ),
    ]
