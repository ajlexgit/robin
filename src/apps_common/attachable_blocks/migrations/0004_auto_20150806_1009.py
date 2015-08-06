# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0003_auto_20150806_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_model',
            field=models.CharField(editable=False, choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], max_length=255, verbose_name='block model'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_model',
            field=models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], max_length=255, verbose_name='block model'),
            preserve_default=True,
        ),
    ]
