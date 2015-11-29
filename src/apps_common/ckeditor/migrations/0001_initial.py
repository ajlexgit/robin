# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, aspects='on_page', storage=libs.media_storage.MediaStorage('page_photos'), variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'format': 'JPEG', 'size': (600, 340)}}, blank=True, min_dimensions=(600, 340), verbose_name='image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'), variations={'admin_thumbnail': {'stretch': False, 'crop': False, 'size': (150, 85)}}, blank=True, verbose_name='image', max_source_dimensions=(1024, 1024))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
