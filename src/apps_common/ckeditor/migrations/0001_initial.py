# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', min_dimensions=(600, 340), storage=libs.media_storage.MediaStorage('page_photos'), variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'format': 'JPEG', 'size': (600, 340)}}, aspects='on_page', blank=True, upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.media_storage.MediaStorage('simple_photos'), variations={'admin_thumbnail': {'crop': False, 'size': (150, 85), 'stretch': False}}, aspects=(), max_source_dimensions=(1024, 1024), blank=True, upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
    ]
