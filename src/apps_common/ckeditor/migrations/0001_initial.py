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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('file', models.FileField(verbose_name='file', storage=libs.storages.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.page_file_filename, blank=True)),
            ],
            options={
                'verbose_name': 'page file',
                'verbose_name_plural': 'page files',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage('page_photos'), blank=True, variations={'wide': {'size': (1440, 990), 'stretch': True}, 'admin_thumbnail': {'size': (240, 165)}, 'normal': {'size': (1024, 704)}, 'mobile': {'size': (768, 528)}}, min_dimensions=(1024, 768), aspects='normal', upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name': 'page photo',
                'verbose_name_plural': 'page photos',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', max_source_dimensions=(3072, 3072), storage=libs.storages.media_storage.MediaStorage('simple_photos'), blank=True, variations={'mobile': {'max_width': 512, 'size': (0, 0), 'crop': False}}, aspects=(), upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name': 'simple photo',
                'verbose_name_plural': 'simple photos',
                'default_permissions': (),
            },
        ),
    ]
