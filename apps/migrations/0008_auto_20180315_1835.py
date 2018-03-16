# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20180315_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompeteQuiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question', models.TextField(max_length=1000)),
                ('option1', models.CharField(max_length=500)),
                ('option2', models.CharField(max_length=500)),
                ('option3', models.CharField(max_length=500)),
                ('option4', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('category', models.ForeignKey(to='apps.Category')),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='level',
            field=models.CharField(max_length=20, default='NONE', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]),
        ),
    ]
