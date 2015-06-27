# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.ckeditor.models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, verbose_name='image', storage=libs.media_storage.MediaStorage('page_photos'), aspects='on_page', min_dimensions=(600, 340), variations={'on_page': {'size': (600, 340), 'format': 'JPEG'}, 'admin_thumbnail': {'size': (150, 85)}}, upload_to=libs.ckeditor.models.page_photo_filename)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, max_source_dimensions=(1024, 1024), verbose_name='image', storage=libs.media_storage.MediaStorage('simple_photos'), aspects=(), variations={'admin_thumbnail': {'action': 3, 'size': (150, 85)}}, upload_to=libs.ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
