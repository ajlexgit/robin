# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mainpageconfig_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='address',
        ),
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='coords',
        ),
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='coords2',
        ),
    ]
