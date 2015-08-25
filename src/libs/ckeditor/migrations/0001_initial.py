# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields
import libs.ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(min_dimensions=(600, 340), variations={'on_page': {'format': 'JPEG', 'size': (600, 340)}, 'admin_thumbnail': {'size': (150, 85)}}, aspects='on_page', blank=True, storage=libs.media_storage.MediaStorage('page_photos'), upload_to=libs.ckeditor.models.page_photo_filename, verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(max_source_dimensions=(1024, 1024), variations={'admin_thumbnail': {'size': (150, 85), 'action': 3}}, aspects=(), blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=libs.ckeditor.models.page_photo_filename, verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
