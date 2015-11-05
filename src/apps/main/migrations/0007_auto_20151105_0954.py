# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151105_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientformmodel',
            name='count',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='count', max_length=2, default=1),
        ),
    ]
