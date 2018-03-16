# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_category_cat_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_img',
            field=models.ImageField(default='category_image/default.png', upload_to='category_image'),
        ),
    ]
