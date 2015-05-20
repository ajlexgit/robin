# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yandex_maps.fields
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('address', models.CharField(max_length=255, verbose_name='адрес', blank=True)),
                ('coords', yandex_maps.fields.YandexCoordsField(null=True, verbose_name='координаты', blank=True)),
                ('coords2', google_maps.fields.GoogleCoordsField(null=True, verbose_name='координаты', blank=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
    ]
