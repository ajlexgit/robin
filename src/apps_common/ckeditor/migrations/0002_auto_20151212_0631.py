# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, min_dimensions=(800, 450), verbose_name='image', blank=True, storage=libs.media_storage.MediaStorage('page_photos'), variations={'mobile': {'size': (512, 288)}, 'admin_thumbnail': {'size': (224, 126)}, 'normal': {'size': (800, 450)}}, aspects='on_page'),
        ),
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.page_photo_filename, verbose_name='image', blank=True, storage=libs.media_storage.MediaStorage('simple_photos'), variations={'mobile': {'size': (0, 0), 'max_width': 512, 'crop': False}, 'admin_thumbnail': {'size': (0, 0), 'max_width': 250, 'max_height': 250, 'crop': False}}, aspects=()),
        ),
    ]
