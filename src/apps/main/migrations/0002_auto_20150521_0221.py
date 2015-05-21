# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import google_maps.fields
import yandex_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='changed', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='address',
            field=models.CharField(blank=True, verbose_name='address', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='coords',
            field=yandex_maps.fields.YandexCoordsField(null=True, blank=True, verbose_name='coordinates'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='coords2',
            field=google_maps.fields.GoogleCoordsField(null=True, blank=True, verbose_name='coordinates'),
            preserve_default=True,
        ),
    ]
