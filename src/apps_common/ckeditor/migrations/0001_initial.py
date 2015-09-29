# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import ckeditor.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'size': (600, 340), 'format': 'JPEG'}}, storage=libs.media_storage.MediaStorage('page_photos'), blank=True, min_dimensions=(600, 340), upload_to=ckeditor.models.page_photo_filename, aspects='on_page')),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', max_source_dimensions=(1024, 1024), variations={'admin_thumbnail': {'crop': False, 'size': (150, 85), 'stretch': False}}, storage=libs.media_storage.MediaStorage('simple_photos'), blank=True, upload_to=ckeditor.models.page_photo_filename, aspects=())),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
    ]
