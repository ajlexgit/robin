# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('file', models.FileField(blank=True, verbose_name='file', upload_to=ckeditor.models.page_file_filename, storage=libs.storages.media_storage.MediaStorage('page_files'))),
            ],
            options={
                'verbose_name_plural': 'page files',
                'verbose_name': 'page file',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', min_dimensions=(900, 500), storage=libs.storages.media_storage.MediaStorage('page_photos'), blank=True, variations={'wide': {'quality': 95, 'crop': False, 'size': (0, 0), 'max_width': 1440}, 'normal': {'size': (0, 0), 'crop': False, 'max_width': 800}, 'mobile': {'size': (0, 0), 'crop': False, 'max_width': 480}, 'admin_thumbnail': {'size': (234, 130)}}, upload_to=ckeditor.models.page_photo_filename, aspects=())),
            ],
            options={
                'verbose_name_plural': 'page photos',
                'verbose_name': 'page photo',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage('simple_photos'), blank=True, variations={'mobile': {'size': (0, 0), 'crop': False, 'max_width': 512}}, upload_to=ckeditor.models.page_photo_filename, max_source_dimensions=(3072, 3072), aspects=())),
            ],
            options={
                'verbose_name_plural': 'simple photos',
                'verbose_name': 'simple photo',
                'default_permissions': ('change',),
            },
        ),
    ]
