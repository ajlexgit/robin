# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shopproduct_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopproduct',
            options={'ordering': ('-created',), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterField(
            model_name='shopcategory',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='visible', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='shopproduct',
            index_together=set([('category', 'is_visible')]),
        ),
        migrations.RemoveField(
            model_name='shopproduct',
            name='sort_order',
        ),
    ]
