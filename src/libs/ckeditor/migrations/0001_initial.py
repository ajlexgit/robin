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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'size': (600, 340), 'format': 'JPEG'}}, upload_to=libs.ckeditor.models.page_photo_filename, blank=True, storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(600, 340), aspects='on_page')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85), 'action': 3}}, upload_to=libs.ckeditor.models.page_photo_filename, blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), max_source_dimensions=(1024, 1024), aspects=())),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
