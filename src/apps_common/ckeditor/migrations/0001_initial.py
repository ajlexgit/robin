# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.models
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('file', models.FileField(storage=libs.storages.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.split_by_dirs, blank=True, verbose_name='file')),
            ],
            options={
                'verbose_name_plural': 'page files',
                'default_permissions': (),
                'verbose_name': 'page file',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.split_by_dirs, min_dimensions=(1024, 768), blank=True, verbose_name='image', variations={'wide': {'max_width': 1440, 'crop': False, 'quality': 95, 'size': (0, 0)}, 'mobile': {'max_width': 480, 'crop': False, 'size': (0, 0)}, 'normal': {'max_width': 800, 'crop': False, 'size': (0, 0)}}, storage=libs.storages.media_storage.MediaStorage('page_photos'), aspects='normal')),
                ('photo_crop', models.CharField(max_length=32, editable=False, blank=True, verbose_name='crop')),
            ],
            options={
                'verbose_name_plural': 'page photos',
                'default_permissions': (),
                'verbose_name': 'page photo',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.split_by_dirs, blank=True, max_source_dimensions=(3072, 3072), verbose_name='image', variations={'mobile': {'max_width': 512, 'crop': False, 'size': (0, 0)}}, storage=libs.storages.media_storage.MediaStorage('simple_photos'), aspects=())),
            ],
            options={
                'verbose_name_plural': 'simple photos',
                'default_permissions': (),
                'verbose_name': 'simple photo',
            },
        ),
    ]
