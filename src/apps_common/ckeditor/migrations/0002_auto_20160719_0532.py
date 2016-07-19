# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import ckeditor.models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(aspects=(), variations={'admin_thumbnail': {'size': (240, 180)}, 'wide': {'stretch': True, 'size': (1440, 1080)}, 'mobile': {'size': (768, 576)}, 'normal': {'size': (1024, 768)}}, storage=libs.storages.media_storage.MediaStorage('page_photos'), min_dimensions=(1024, 768), blank=True, upload_to=ckeditor.models.page_photo_filename, verbose_name='image'),
        ),
    ]
