# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_auto_20180316_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_img',
            field=models.ImageField(default='category_image/default.png', upload_to=apps.models.get_image_name, width_field=368, height_field=245),
        ),
    ]
