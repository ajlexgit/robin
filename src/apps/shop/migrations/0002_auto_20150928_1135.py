# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopproduct',
            options={'verbose_name_plural': 'products', 'ordering': ('is_visible', 'category', 'sort_order'), 'verbose_name': 'product'},
        ),
    ]
