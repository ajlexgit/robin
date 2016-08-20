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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('file', models.FileField(verbose_name='file', upload_to=ckeditor.models.split_by_dirs, storage=libs.storages.media_storage.MediaStorage('page_files'), blank=True)),
            ],
            options={
                'verbose_name': 'page file',
                'default_permissions': (),
                'verbose_name_plural': 'page files',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='normal', upload_to=ckeditor.models.split_by_dirs, storage=libs.storages.media_storage.MediaStorage('page_photos'), variations={'mobile': {'crop': False, 'max_width': 480, 'size': (0, 0)}, 'normal': {'crop': False, 'max_width': 800, 'size': (0, 0)}, 'wide': {'crop': False, 'max_width': 1440, 'quality': 95, 'size': (0, 0)}}, verbose_name='image', blank=True, min_dimensions=(1024, 768))),
                ('photo_crop', models.CharField(editable=False, verbose_name='crop', blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'page photo',
                'default_permissions': (),
                'verbose_name_plural': 'page photos',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), upload_to=ckeditor.models.split_by_dirs, storage=libs.storages.media_storage.MediaStorage('simple_photos'), variations={'mobile': {'crop': False, 'max_width': 512, 'size': (0, 0)}}, verbose_name='image', blank=True, max_source_dimensions=(3072, 3072))),
            ],
            options={
                'verbose_name': 'simple photo',
                'default_permissions': (),
                'verbose_name_plural': 'simple photos',
            },
        ),
    ]
