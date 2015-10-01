# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(600, 340), aspects='on_page', variations={'on_page': {'format': 'JPEG', 'size': (600, 340)}, 'admin_thumbnail': {'size': (150, 85)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image', storage=libs.media_storage.MediaStorage('page_photos'))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), variations={'admin_thumbnail': {'crop': False, 'stretch': False, 'size': (150, 85)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image', max_source_dimensions=(1024, 1024), storage=libs.media_storage.MediaStorage('simple_photos'))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
