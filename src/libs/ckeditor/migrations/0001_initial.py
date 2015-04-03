# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.ckeditor.models
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'format': 'JPEG', 'size': (600, 340)}}, upload_to=libs.ckeditor.models.page_photo_filename, blank=True, aspects='on_page', storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(600, 340))),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', variations={'admin_thumbnail': {'action': 4, 'size': (150, 85)}}, upload_to=libs.ckeditor.models.page_photo_filename, max_source_dimensions=(1024, 1024), blank=True, aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
