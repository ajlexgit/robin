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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', aspects='on_page', variations={'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}, 'mobile': {'size': (512, 288)}}, blank=True, min_dimensions=(800, 450), storage=libs.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('app_name', models.CharField(verbose_name='application', blank=True, max_length=30)),
                ('model_name', models.CharField(verbose_name='model', blank=True, max_length=30)),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('photo', libs.stdimage.fields.StdImageField(verbose_name='image', aspects=(), variations={'admin_thumbnail': {'max_width': 250, 'max_height': 250, 'size': (0, 0), 'crop': False}, 'mobile': {'max_width': 512, 'size': (0, 0), 'crop': False}}, blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'default_permissions': ('change',),
            },
        ),
    ]
