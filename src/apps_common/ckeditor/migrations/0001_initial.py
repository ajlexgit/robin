# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, upload_to=ckeditor.models.page_photo_filename, aspects='on_page', variations={'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}, 'mobile': {'size': (512, 288)}}, min_dimensions=(800, 450), storage=libs.media_storage.MediaStorage('page_photos'), verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'page photos',
                'default_permissions': ('change',),
                'verbose_name': 'page photo',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(default=0, db_index=True, verbose_name='entry id')),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, upload_to=ckeditor.models.page_photo_filename, aspects=(), variations={'admin_thumbnail': {'crop': False, 'size': (0, 0), 'max_height': 250, 'max_width': 250}, 'mobile': {'crop': False, 'size': (0, 0), 'max_width': 512}}, storage=libs.media_storage.MediaStorage('simple_photos'), verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'simple photos',
                'default_permissions': ('change',),
                'verbose_name': 'simple photo',
            },
        ),
    ]
