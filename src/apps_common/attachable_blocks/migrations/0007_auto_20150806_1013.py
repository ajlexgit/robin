# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0006_auto_20150806_1011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachableblock',
            old_name='block_key',
            new_name='block_type',
        ),
        migrations.RenameField(
            model_name='attachableblockref',
            old_name='block_key',
            new_name='block_type',
        ),
        migrations.AlterUniqueTogether(
            name='attachableblockref',
            unique_together=set([]),
        ),
    ]
