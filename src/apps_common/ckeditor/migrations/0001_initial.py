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
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(600, 340), aspects='on_page', variations={'on_page': {'format': 'JPEG', 'size': (600, 340)}, 'admin_thumbnail': {'size': (150, 85)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('simple_photos'), aspects=(), variations={'admin_thumbnail': {'crop': False, 'stretch': False, 'size': (150, 85)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, max_source_dimensions=(1024, 1024), verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
