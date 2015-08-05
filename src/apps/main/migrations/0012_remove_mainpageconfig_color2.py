# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150804_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='color2',
        ),
    ]
