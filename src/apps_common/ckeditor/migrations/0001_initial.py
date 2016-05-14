# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('file', models.FileField(blank=True, upload_to=ckeditor.models.page_file_filename, storage=libs.media_storage.MediaStorage('page_files'), verbose_name='file')),
            ],
            options={
                'verbose_name_plural': 'page files',
                'default_permissions': ('change',),
                'verbose_name': 'page file',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(900, 500), variations={'wide': {'quality': 95, 'crop': False, 'size': (0, 0), 'max_width': 1440}, 'admin_thumbnail': {'size': (234, 130)}, 'mobile': {'crop': False, 'size': (0, 0), 'max_width': 480}, 'normal': {'crop': False, 'size': (0, 0), 'max_width': 800}}, storage=libs.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', blank=True, aspects=())),
            ],
            options={
                'verbose_name_plural': 'page photos',
                'default_permissions': ('change',),
                'verbose_name': 'page photo',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(variations={'mobile': {'crop': False, 'size': (0, 0), 'max_width': 512}}, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', blank=True, aspects=(), max_source_dimensions=(3072, 3072))),
            ],
            options={
                'verbose_name_plural': 'simple photos',
                'default_permissions': ('change',),
                'verbose_name': 'simple photo',
            },
        ),
    ]
