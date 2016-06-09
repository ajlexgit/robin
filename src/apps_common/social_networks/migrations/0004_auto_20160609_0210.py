# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0003_auto_20160609_0204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialpost',
            options={'verbose_name_plural': 'posts', 'verbose_name': 'post', 'ordering': ('-scheduled', '-created')},
        ),
    ]
