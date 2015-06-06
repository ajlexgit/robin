# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mainpageconfig_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
            preserve_default=True,
        ),
    ]
