# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import google_maps.fields
import yandex_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mainpageconfig_coords2'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientformmodel',
            name='coords',
            field=google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True),
        ),
        migrations.AddField(
            model_name='clientformmodel',
            name='coords2',
            field=yandex_maps.fields.YandexCoordsField(verbose_name='coords2', blank=True),
        ),
    ]
