# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150924_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, related_name='children', null=True, to='shop.Category', verbose_name='parent category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='sort_order',
            field=models.PositiveIntegerField(verbose_name='sort order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='sort_order',
            field=models.PositiveIntegerField(verbose_name='sort order'),
            preserve_default=True,
        ),
    ]
