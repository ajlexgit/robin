# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20151113_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoporder',
            name='is_archived',
            field=models.BooleanField(verbose_name='archived', default=False),
        ),
    ]
