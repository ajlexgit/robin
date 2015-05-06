# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='counter',
            name='title',
            field=models.CharField(default='', max_length=128, verbose_name='title'),
            preserve_default=False,
        ),
    ]
