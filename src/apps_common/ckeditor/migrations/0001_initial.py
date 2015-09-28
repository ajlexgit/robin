# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, min_dimensions=(600, 340), storage=libs.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'on_page': {'size': (600, 340), 'format': 'JPEG'}, 'admin_thumbnail': {'size': (150, 85)}}, aspects='on_page')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85), 'stretch': False, 'crop': False}}, aspects=(), max_source_dimensions=(1024, 1024))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
