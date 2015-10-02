# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_auto_20151001_1250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachableblock',
            options={'verbose_name_plural': 'attachable blocks', 'verbose_name': 'attachable block', 'ordering': ('label',)},
        ),
        migrations.AlterModelOptions(
            name='attachablereference',
            options={'verbose_name_plural': 'attached blocks', 'verbose_name': 'attached block', 'ordering': ('set_name', 'sort_order')},
        ),
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(editable=False, max_length=255, verbose_name='block type', choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')]),
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='block_type',
            field=models.CharField(max_length=255, verbose_name='block type', choices=[('main.mainblockfirst', 'First block type'), ('main.mainblocksecond', 'Second block type')]),
        ),
    ]
