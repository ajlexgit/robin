# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20150825_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentvote',
            name='value',
            field=models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')]),
            preserve_default=True,
        ),
    ]
