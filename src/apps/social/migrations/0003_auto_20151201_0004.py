# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20151201_0000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followusblock',
            options={'verbose_name_plural': 'Follow us', 'verbose_name': 'Follow us'},
        ),
    ]
