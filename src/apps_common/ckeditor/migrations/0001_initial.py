# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import ckeditor.models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('file', models.FileField(storage=libs.storages.media_storage.MediaStorage('page_files'), verbose_name='file', upload_to=ckeditor.models.page_file_filename, blank=True)),
            ],
            options={
                'verbose_name': 'page file',
                'default_permissions': ('change',),
                'verbose_name_plural': 'page files',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('page_photos'), verbose_name='image', upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'size': (234, 130)}, 'wide': {'quality': 95, 'max_width': 1440, 'crop': False, 'size': (0, 0)}, 'normal': {'max_width': 800, 'crop': False, 'size': (0, 0)}, 'mobile': {'max_width': 480, 'crop': False, 'size': (0, 0)}}, aspects=(), min_dimensions=(900, 500), blank=True)),
            ],
            options={
                'verbose_name': 'page photo',
                'default_permissions': ('change',),
                'verbose_name_plural': 'page photos',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('simple_photos'), verbose_name='image', upload_to=ckeditor.models.page_photo_filename, variations={'mobile': {'max_width': 512, 'crop': False, 'size': (0, 0)}}, max_source_dimensions=(3072, 3072), aspects=(), blank=True)),
            ],
            options={
                'verbose_name': 'simple photo',
                'default_permissions': ('change',),
                'verbose_name_plural': 'simple photos',
            },
        ),
    ]
