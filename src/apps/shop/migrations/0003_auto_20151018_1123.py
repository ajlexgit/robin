# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20151018_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopconfig',
            name='header',
            field=models.CharField(max_length=128, verbose_name='header'),
        ),
    ]
