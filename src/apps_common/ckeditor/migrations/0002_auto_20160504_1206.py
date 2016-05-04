# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, verbose_name='image', aspects=(), blank=True, variations={'mobile': {'max_width': 480, 'size': (0, 0), 'crop': False}, 'admin_thumbnail': {'size': (234, 130)}, 'normal': {'max_width': 800, 'size': (0, 0), 'crop': False}, 'wide': {'max_width': 1440, 'size': (0, 0), 'crop': False, 'quality': 95}}, storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(900, 500)),
        ),
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, verbose_name='image', aspects=(), blank=True, variations={'mobile': {'max_width': 512, 'size': (0, 0), 'crop': False}}, storage=libs.media_storage.MediaStorage('simple_photos')),
        ),
    ]
