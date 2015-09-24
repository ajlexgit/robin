# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories', 'verbose_name': 'category'},
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(db_index=True, editable=False, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, editable=False, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(verbose_name='parent category', null=True, to='shop.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, editable=False, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, editable=False, default=0),
            preserve_default=False,
        ),
    ]
