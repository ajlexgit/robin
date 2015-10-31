# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yandex_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151031_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords2',
            field=yandex_maps.fields.YandexCoordsField(blank=True, verbose_name='coords2'),
        ),
    ]
