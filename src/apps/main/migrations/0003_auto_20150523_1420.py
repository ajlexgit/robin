# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150521_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='change date'),
            preserve_default=True,
        ),
    ]
