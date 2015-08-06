# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0007_auto_20150806_1013'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_type')]),
        ),
    ]
