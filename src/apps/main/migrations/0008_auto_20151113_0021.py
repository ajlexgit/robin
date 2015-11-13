# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20151105_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientformmodel',
            name='count',
            field=models.PositiveIntegerField(default=1, verbose_name='count', validators=[django.core.validators.MaxValueValidator(99)]),
        ),
    ]
