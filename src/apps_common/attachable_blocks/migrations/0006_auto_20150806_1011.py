# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20150806_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_key',
            field=models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], editable=False, verbose_name='block type', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_key',
            field=models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], verbose_name='block type', max_length=255),
            preserve_default=True,
        ),
    ]
