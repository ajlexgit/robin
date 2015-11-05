# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151103_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientformmodel',
            name='count',
            field=models.PositiveIntegerField(verbose_name='count', default=1),
        ),
    ]
