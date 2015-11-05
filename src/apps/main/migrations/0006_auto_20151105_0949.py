# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_clientformmodel_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientformmodel',
            name='count',
            field=models.PositiveIntegerField(verbose_name='count', max_length=2, default=1),
        ),
    ]
