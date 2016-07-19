# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0002_auto_20160719_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(variations={'mobile': {'size': (768, 528)}, 'wide': {'stretch': True, 'size': (1440, 990)}, 'admin_thumbnail': {'size': (240, 165)}, 'normal': {'size': (1024, 704)}}, storage=libs.storages.media_storage.MediaStorage('page_photos'), upload_to=ckeditor.models.page_photo_filename, verbose_name='image', blank=True, aspects='normal', min_dimensions=(1024, 768)),
        ),
    ]
