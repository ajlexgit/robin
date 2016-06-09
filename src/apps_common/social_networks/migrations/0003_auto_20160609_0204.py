# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0002_auto_20160609_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialpost',
            name='modified',
        ),
        migrations.AddField(
            model_name='socialpost',
            name='scheduled',
            field=models.BooleanField(default=True, verbose_name='sheduled for sharing'),
        ),
    ]
