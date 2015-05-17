# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yandex_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150502_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='адрес'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords',
            field=yandex_maps.fields.YandexCoordsField(blank=True, verbose_name='координаты', null=True),
            preserve_default=True,
        ),
    ]
