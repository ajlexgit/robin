# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.models
import libs.storages.media_storage
import libs.file_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('file', libs.file_field.fields.FileField(blank=True, upload_to=ckeditor.models.split_by_dirs, verbose_name='file', storage=libs.storages.media_storage.MediaStorage('page_files'))),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'page files',
                'verbose_name': 'page file',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, upload_to=ckeditor.models.split_by_dirs, aspects='normal', variations={'normal': {'size': (800, 450)}, 'wide': {'quality': 88, 'size': (1024, 576)}, 'mobile': {'size': (480, 270)}}, min_dimensions=(800, 450), verbose_name='image', storage=libs.storages.media_storage.MediaStorage('page_photos'))),
                ('photo_crop', models.CharField(blank=True, max_length=32, verbose_name='crop', editable=False)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'page photos',
                'verbose_name': 'page photo',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, upload_to=ckeditor.models.split_by_dirs, max_source_dimensions=(3072, 3072), aspects=(), variations={'mobile': {'max_width': 512, 'crop': False, 'size': (0, 0)}}, verbose_name='image', storage=libs.storages.media_storage.MediaStorage('simple_photos'))),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'simple photos',
                'verbose_name': 'simple photo',
            },
        ),
    ]
