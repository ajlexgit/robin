# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_auto_20150928_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='label',
            field=models.CharField(max_length=128, verbose_name='label'),
        ),
    ]
