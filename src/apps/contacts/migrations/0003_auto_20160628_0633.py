# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20160628_0325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactsconfig',
            options={'default_permissions': ('change',), 'verbose_name': 'settings'},
        ),
    ]
