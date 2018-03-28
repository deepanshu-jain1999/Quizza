# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0016_auto_20180323_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyInstruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('instr', models.CharField(max_length=200, blank=True)),
            ],
        ),
    ]
