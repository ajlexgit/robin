# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='on_page', min_dimensions=(600, 340), variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'format': 'JPEG', 'size': (600, 340)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('page_photos'), verbose_name='image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), variations={'admin_thumbnail': {'size': (150, 85), 'stretch': False, 'crop': False}}, blank=True, upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('simple_photos'), verbose_name='image', max_source_dimensions=(1024, 1024))),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
