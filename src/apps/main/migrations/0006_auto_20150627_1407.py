# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yandex_maps.fields
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_inlinesample'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords',
            field=yandex_maps.fields.YandexCoordsField(blank=True, verbose_name='coords'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(blank=True, null=True, verbose_name='color'),
            preserve_default=True,
        ),
    ]
