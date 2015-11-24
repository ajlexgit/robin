# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainblockfirst',
            name='attachableblock_ptr',
        ),
        migrations.RemoveField(
            model_name='mainblocksecond',
            name='attachableblock_ptr',
        ),
        migrations.DeleteModel(
            name='MainBlockFirst',
        ),
        migrations.DeleteModel(
            name='MainBlockSecond',
        ),
    ]
