# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0004_auto_20150924_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='sort_order',
            field=models.PositiveIntegerField(verbose_name='sort order', default=0),
            preserve_default=True,
        ),
    ]
