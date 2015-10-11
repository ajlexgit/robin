# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.models
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, storage=libs.media_storage.MediaStorage('page_photos'), aspects='on_page', verbose_name='image', variations={'on_page': {'size': (600, 340), 'format': 'JPEG'}, 'admin_thumbnail': {'size': (150, 85)}}, upload_to=ckeditor.models.page_photo_filename, min_dimensions=(600, 340))),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), aspects=(), verbose_name='image', variations={'admin_thumbnail': {'crop': False, 'stretch': False, 'size': (150, 85)}}, upload_to=ckeditor.models.page_photo_filename, max_source_dimensions=(1024, 1024))),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
    ]
