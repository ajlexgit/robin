# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_mainpageconfig_color2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inlinesample',
            name='color',
        ),
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='color',
        ),
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='color2',
        ),
    ]
