# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'ordering': ('is_visible', 'sort_order'), 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'product', 'ordering': ('is_visible', 'sort_order'), 'verbose_name_plural': 'products'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='order',
            new_name='sort_order',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='order',
            new_name='sort_order',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Not paid'), (2, 'Paid')], default=1),
            preserve_default=True,
        ),
    ]
