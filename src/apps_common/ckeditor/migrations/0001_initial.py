# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('file', models.FileField(upload_to=ckeditor.models.page_file_filename, verbose_name='file', storage=libs.media_storage.MediaStorage('page_files'), blank=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'page files',
                'verbose_name': 'page file',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='normal', min_dimensions=(960, 540), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'admin_thumbnail': {'size': (224, 126)}, 'mobile': {'size': (512, 288)}, 'wide': {'size': (1440, 810), 'stretch': True}, 'normal': {'size': (960, 540)}}, storage=libs.media_storage.MediaStorage('page_photos'), blank=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'page photos',
                'verbose_name': 'page photo',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), max_source_dimensions=(2048, 2048), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'admin_thumbnail': {'size': (0, 0), 'max_height': 250, 'max_width': 250, 'crop': False}, 'mobile': {'size': (0, 0), 'max_width': 512, 'crop': False}}, storage=libs.media_storage.MediaStorage('simple_photos'), blank=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'simple photos',
                'verbose_name': 'simple photo',
            },
        ),
    ]
