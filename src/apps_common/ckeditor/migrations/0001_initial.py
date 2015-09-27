# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, verbose_name='image', min_dimensions=(600, 340), aspects='on_page', storage=libs.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'size': (600, 340), 'format': 'JPEG'}})),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, verbose_name='image', max_source_dimensions=(1024, 1024), aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename, variations={'admin_thumbnail': {'size': (150, 85), 'stretch': False, 'crop': False}})),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
