# Generated by Django 2.0 on 2018-04-11 18:22

import apps.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=1000)),
                ('option1', models.CharField(max_length=500)),
                ('option2', models.CharField(max_length=500)),
                ('option3', models.CharField(max_length=500)),
                ('option4', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Category')),
            ],
        ),
        migrations.CreateModel(
            name='EasyInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instr', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HardInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instr', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MediumInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instr', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_pic', models.ImageField(default='profile_pic/default.jpg', upload_to=apps.models.upload_profile_image)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='NONE', max_length=20)),
                ('question', models.TextField(max_length=1000)),
                ('option1', models.CharField(max_length=500)),
                ('option2', models.CharField(max_length=500)),
                ('option3', models.CharField(max_length=500)),
                ('option4', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_score', models.FloatField(default=0.0)),
                ('easy_score', models.FloatField(default=0.0)),
                ('medium_score', models.FloatField(default=0.0)),
                ('hard_score', models.FloatField(default=0.0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
