# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20151105_0726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopproduct',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='shopproduct',
            name='photo_crop',
        ),
    ]
