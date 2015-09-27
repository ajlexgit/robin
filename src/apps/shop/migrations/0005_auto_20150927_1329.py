# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20150927_1318'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='ShopOrder',
        ),
    ]
