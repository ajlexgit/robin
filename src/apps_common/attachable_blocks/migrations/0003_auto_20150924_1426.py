# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_auto_20150924_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_type',
            field=models.CharField(max_length=255, choices=[('blocks.mainsliderblock', 'MainSlider Blocks'), ('blocks.suppliersblock', 'Suppliers blocks')], editable=False, verbose_name='block type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='block_type',
            field=models.CharField(max_length=255, choices=[('blocks.mainsliderblock', 'MainSlider Blocks'), ('blocks.suppliersblock', 'Suppliers blocks')], verbose_name='block type'),
            preserve_default=True,
        ),
    ]
