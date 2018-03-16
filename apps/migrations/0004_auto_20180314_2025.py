# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_quiz_played_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='played_user',
        ),
        migrations.AddField(
            model_name='quiz',
            name='mode',
            field=models.CharField(max_length=17, default='NONE', choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')]),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.OneToOneField(to='apps.Category'),
        ),
    ]
