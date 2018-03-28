# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0022_auto_20180328_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.CharField(max_length=200)),
                ('cat_img', models.ImageField(default='category_image/default.png', help_text='Aspect ratio must be near 3;2', upload_to=apps.models.get_image_name)),
                ('time_per_ques_easy', models.IntegerField(default=20)),
                ('time_per_ques_medium', models.IntegerField(default=40)),
                ('time_per_ques_hard', models.IntegerField(default=60)),
            ],
        ),
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
        migrations.CreateModel(
            name='EasyInstruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('instr', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HardInstruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('instr', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediumInstruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('instr', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('level', models.CharField(max_length=20, default='NONE', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])),
                ('question', models.TextField(max_length=1000)),
                ('option1', models.CharField(max_length=500)),
                ('option2', models.CharField(max_length=500)),
                ('option3', models.CharField(max_length=500)),
                ('option4', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('category', models.ForeignKey(to='apps.Category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='easy_instr',
            field=models.ManyToManyField(to='apps.EasyInstruction'),
        ),
        migrations.AddField(
            model_name='category',
            name='hard_instr',
            field=models.ManyToManyField(to='apps.HardInstruction'),
        ),
        migrations.AddField(
            model_name='category',
            name='medium_instr',
            field=models.ManyToManyField(to='apps.MediumInstruction'),
        ),
    ]
