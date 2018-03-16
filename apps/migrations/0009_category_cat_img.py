# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_auto_20180315_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_img',
            field=models.ImageField(blank=True, upload_to='category_image'),
        ),
    ]
