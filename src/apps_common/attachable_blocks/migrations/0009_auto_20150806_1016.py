# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0008_auto_20150806_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(choices=[('main.mainblocksecond', 'Second block type'), ('main.mainblockfirst', 'First block type')], max_length=255, editable=False, verbose_name='block type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_type',
            field=models.CharField(choices=[('main.mainblocksecond', 'Second block type'), ('main.mainblockfirst', 'First block type')], max_length=255, verbose_name='block type'),
            preserve_default=True,
        ),
    ]
