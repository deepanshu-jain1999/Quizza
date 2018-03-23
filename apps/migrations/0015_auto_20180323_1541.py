# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0014_auto_20180316_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_img',
            field=models.ImageField(default='category_image/default.png', help_text='Aspect ratio must be near 3;2', upload_to=apps.models.get_image_name),
        ),
    ]
