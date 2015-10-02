# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', aspects='on_page', storage=libs.media_storage.MediaStorage('page_photos'), variations={'on_page': {'size': (600, 340), 'format': 'JPEG'}, 'admin_thumbnail': {'size': (150, 85)}}, upload_to=ckeditor.models.page_photo_filename, blank=True, min_dimensions=(600, 340))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'), max_source_dimensions=(1024, 1024), variations={'admin_thumbnail': {'crop': False, 'stretch': False, 'size': (150, 85)}}, upload_to=ckeditor.models.page_photo_filename, blank=True)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
