# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.models
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, min_dimensions=(600, 340), variations={'on_page': {'format': 'JPEG', 'size': (600, 340)}, 'admin_thumbnail': {'size': (150, 85)}}, blank=True, verbose_name='image', storage=libs.media_storage.MediaStorage('page_photos'), aspects='on_page')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'stretch': False, 'size': (150, 85), 'crop': False}}, max_source_dimensions=(1024, 1024), blank=True, verbose_name='image', storage=libs.media_storage.MediaStorage('simple_photos'), aspects=())),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
