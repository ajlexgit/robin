# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('blocks', '0002_mainblockfirst_mainblocksecond'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myblock',
            name='attachableblock_ptr',
        ),
        migrations.DeleteModel(
            name='MyBlock',
        ),
    ]
