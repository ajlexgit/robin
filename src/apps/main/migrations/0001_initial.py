# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import yandex_maps.fields
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('preview', libs.stdimage.fields.StdImageField(min_dimensions=(400, 300), aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview'), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, verbose_name='preview', upload_to='')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('address', models.CharField(verbose_name='address', max_length=255, blank=True)),
                ('coords', yandex_maps.fields.YandexCoordsField(verbose_name='coordinates', null=True, blank=True)),
                ('coords2', google_maps.fields.GoogleCoordsField(verbose_name='coordinates', null=True, blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
    ]
