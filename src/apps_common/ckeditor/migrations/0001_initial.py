# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='on_page', blank=True, min_dimensions=(600, 340), verbose_name='image', variations={'on_page': {'format': 'JPEG', 'size': (600, 340)}, 'admin_thumbnail': {'size': (150, 85)}}, storage=libs.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), blank=True, verbose_name='image', max_source_dimensions=(1024, 1024), variations={'admin_thumbnail': {'crop': False, 'size': (150, 85), 'stretch': False}}, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
