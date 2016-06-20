# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0003_auto_20160620_0233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedpost',
            options={'verbose_name_plural': 'feeds', 'verbose_name': 'feed post', 'ordering': ('-scheduled', '-created')},
        ),
    ]
