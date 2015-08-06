# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0004_auto_20150806_1009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachableblock',
            old_name='block_model',
            new_name='block_key',
        ),
        migrations.RenameField(
            model_name='attachableblockref',
            old_name='block_model',
            new_name='block_key',
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([('content_type', 'object_id', 'block_key')]),
        ),
    ]
