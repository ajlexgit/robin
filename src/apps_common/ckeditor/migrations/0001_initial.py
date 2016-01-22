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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, min_dimensions=(800, 450), storage=libs.media_storage.MediaStorage('page_photos'), variations={'mobile': {'size': (512, 288)}, 'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}}, verbose_name='image', aspects='on_page', blank=True)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(max_length=30, verbose_name='application', blank=True)),
                ('model_name', models.CharField(max_length=30, verbose_name='model', blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', default=0, db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('simple_photos'), variations={'mobile': {'max_width': 512, 'size': (0, 0), 'crop': False}, 'admin_thumbnail': {'max_height': 250, 'size': (0, 0), 'max_width': 250, 'crop': False}}, verbose_name='image', aspects=(), blank=True)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]
