# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields
import google_maps.fields
import libs.media_storage
import yandex_maps.fields
import libs.ckeditor.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color')),
            ],
            options={
                'verbose_name_plural': 'Inline samples',
                'verbose_name': 'Inline sample',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',), min_dimensions=(400, 300), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, upload_to='')),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(null=True, verbose_name='color', blank=True)),
                ('ya_coords', yandex_maps.fields.YandexCoordsField(verbose_name='coords', blank=True)),
                ('go_coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inlinesample',
            name='config',
            field=models.ForeignKey(to='main.MainPageConfig', verbose_name='config'),
            preserve_default=True,
        ),
    ]
