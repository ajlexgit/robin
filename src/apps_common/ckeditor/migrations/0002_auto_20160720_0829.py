# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagephoto',
            name='photo_crop',
            field=models.CharField(verbose_name='crop', editable=False, max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(variations={'mobile': {'max_width': 480, 'crop': False, 'size': (0, 0)}, 'wide': {'quality': 95, 'max_width': 1440, 'size': (0, 0), 'crop': False}, 'normal': {'max_width': 800, 'crop': False, 'size': (0, 0)}}, min_dimensions=(1024, 768), storage=libs.storages.media_storage.MediaStorage('page_photos'), blank=True, upload_to=ckeditor.models.split_by_dirs, verbose_name='image', aspects='normal'),
        ),
    ]
