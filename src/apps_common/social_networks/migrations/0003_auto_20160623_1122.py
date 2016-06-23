# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0002_auto_20160623_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sociallinks',
            options={'default_permissions': ('change',), 'verbose_name': 'Links'},
        ),
    ]
