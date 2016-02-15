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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects='on_page', min_dimensions=(800, 450), variations={'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}, 'mobile': {'size': (512, 288)}}, blank=True, storage=libs.media_storage.MediaStorage('page_photos'), verbose_name='image', upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', models.CharField(verbose_name='application', max_length=30, blank=True)),
                ('model_name', models.CharField(verbose_name='model', max_length=30, blank=True)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(aspects=(), variations={'admin_thumbnail': {'max_width': 250, 'max_height': 250, 'size': (0, 0), 'crop': False}, 'mobile': {'max_width': 512, 'crop': False, 'size': (0, 0)}}, blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), verbose_name='image', upload_to=ckeditor.models.page_photo_filename)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
    ]
