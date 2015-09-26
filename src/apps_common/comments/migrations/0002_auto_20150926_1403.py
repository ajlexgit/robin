# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='order',
        ),
        migrations.AddField(
            model_name='comment',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='sort order', editable=False),
            preserve_default=True,
        ),
    ]
