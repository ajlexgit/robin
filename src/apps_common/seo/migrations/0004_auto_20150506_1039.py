# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0003_counter_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='position',
            field=models.CharField(verbose_name='position', max_length=12, choices=[('head', 'Head'), ('body', 'Body')]),
            preserve_default=True,
        ),
    ]
