# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import ckeditor.models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('file', models.FileField(blank=True, storage=libs.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.page_file_filename, verbose_name='file')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='on_page', storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(960, 540), variations={'normal': {'size': (960, 540)}, 'admin_thumbnail': {'size': (224, 126)}, 'wide': {'size': (1440, 810)}, 'mobile': {'size': (512, 288)}}, upload_to=ckeditor.models.page_photo_filename, blank=True, verbose_name='image')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'), variations={'admin_thumbnail': {'size': (0, 0), 'max_width': 250, 'max_height': 250, 'crop': False}, 'mobile': {'size': (0, 0), 'max_width': 512, 'crop': False}}, upload_to=ckeditor.models.page_photo_filename, blank=True, verbose_name='image', max_source_dimensions=(2048, 2048))),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'simple photos',
                'verbose_name': 'simple photo',
            },
        ),
    ]
