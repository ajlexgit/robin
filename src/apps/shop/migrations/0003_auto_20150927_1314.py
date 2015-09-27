# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150927_1232'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='ShopCategory',
        ),
    ]
