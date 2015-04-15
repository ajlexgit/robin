# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.ckeditor.models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(aspects='on_page', blank=True, verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85)}, 'on_page': {'format': 'JPEG', 'size': (600, 340)}}, storage=libs.media_storage.MediaStorage('page_photos'), upload_to=libs.ckeditor.models.page_photo_filename, min_dimensions=(600, 340))),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(db_index=True, default=0, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), max_source_dimensions=(1024, 1024), blank=True, verbose_name='image', variations={'admin_thumbnail': {'size': (150, 85), 'action': 4}}, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=libs.ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
            bases=(models.Model,),
        ),
    ]
