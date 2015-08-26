# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(verbose_name='block type', editable=False, choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachableblockref',
            name='block_type',
            field=models.CharField(verbose_name='block type', choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], max_length=255),
            preserve_default=True,
        ),
    ]
