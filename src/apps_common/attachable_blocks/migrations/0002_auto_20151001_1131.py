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
            field=models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], verbose_name='block type', max_length=255, editable=False),
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='block_type',
            field=models.CharField(choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')], verbose_name='block type', max_length=255),
        ),
    ]
