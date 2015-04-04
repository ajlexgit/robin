# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import libs.ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'size': (600, 340), 'format': 'JPEG'}}, min_dimensions=(600, 340), storage=libs.media_storage.MediaStorage('page_photos'), aspects='on_page', upload_to=libs.ckeditor.models.page_photo_filename, blank=True, verbose_name='image')),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=30, blank=True, verbose_name='application')),
                ('model_name', models.CharField(max_length=30, blank=True, verbose_name='model')),
                ('instance_id', models.IntegerField(db_index=True, verbose_name='entry id', default=0)),
                ('photo', libs.stdimage.fields.StdImageField(variations={'admin_thumbnail': {'size': (150, 85), 'action': 4}}, storage=libs.media_storage.MediaStorage('simple_photos'), aspects=(), max_source_dimensions=(1024, 1024), upload_to=libs.ckeditor.models.page_photo_filename, blank=True, verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
