# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150924_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitembase',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='sort order'),
            preserve_default=True,
        ),
    ]
