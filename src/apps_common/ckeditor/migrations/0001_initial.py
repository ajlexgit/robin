# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('file', models.FileField(verbose_name='file', storage=libs.storages.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.page_file_filename, blank=True)),
            ],
            options={
                'verbose_name': 'page file',
                'verbose_name_plural': 'page files',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename, min_dimensions=(900, 500), blank=True, variations={'mobile': {'crop': False, 'size': (0, 0), 'max_width': 480}, 'normal': {'crop': False, 'size': (0, 0), 'max_width': 800}, 'wide': {'quality': 95, 'crop': False, 'size': (0, 0), 'max_width': 1440}, 'admin_thumbnail': {'size': (234, 130)}}, aspects=())),
            ],
            options={
                'verbose_name': 'page photo',
                'verbose_name_plural': 'page photos',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename, max_source_dimensions=(3072, 3072), blank=True, variations={'mobile': {'crop': False, 'size': (0, 0), 'max_width': 512}}, aspects=())),
            ],
            options={
                'verbose_name': 'simple photo',
                'verbose_name_plural': 'simple photos',
                'default_permissions': ('change',),
            },
        ),
    ]
