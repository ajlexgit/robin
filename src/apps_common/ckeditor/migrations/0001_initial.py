# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.media_storage.MediaStorage('page_photos'), blank=True, aspects='on_page', upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}, 'mobile': {'size': (512, 288)}}, min_dimensions=(800, 450))),
            ],
            options={
                'verbose_name': 'page photo',
                'verbose_name_plural': 'page photos',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.media_storage.MediaStorage('simple_photos'), max_source_dimensions=(2048, 2048), blank=True, aspects=(), upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'size': (0, 0), 'max_width': 250, 'max_height': 250, 'crop': False}, 'mobile': {'size': (0, 0), 'max_width': 512, 'crop': False}})),
            ],
            options={
                'verbose_name': 'simple photo',
                'verbose_name_plural': 'simple photos',
                'default_permissions': ('change',),
            },
        ),
    ]
