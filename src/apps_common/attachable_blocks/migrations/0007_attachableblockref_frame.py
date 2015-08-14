# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0006_auto_20150814_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachableblockref',
            name='frame',
            field=models.PositiveSmallIntegerField(verbose_name='frame', default=0),
            preserve_default=True,
        ),
    ]
