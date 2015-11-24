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
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(600, 340), storage=libs.media_storage.MediaStorage('page_photos'), aspects='on_page', blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'on_page': {'size': (600, 340), 'format': 'JPEG'}, 'admin_thumbnail': {'size': (150, 85)}})),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('simple_photos'), aspects=(), blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85), 'stretch': False, 'crop': False}}, max_source_dimensions=(1024, 1024))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
