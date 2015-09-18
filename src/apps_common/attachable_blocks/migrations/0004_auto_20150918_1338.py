# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0003_auto_20150918_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachablereference',
            options={'ordering': ('frame', 'order'), 'verbose_name_plural': 'Attached blocks', 'verbose_name': 'Attached block'},
        ),
        migrations.AlterUniqueTogether(
            name='attachablereference',
            unique_together=set([('content_type', 'object_id', 'block_type', 'block', 'frame')]),
        ),
    ]
