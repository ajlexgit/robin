# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150928_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopconfig',
            name='title',
            field=models.CharField(verbose_name='title', default='', max_length=128),
            preserve_default=False,
        ),
    ]
