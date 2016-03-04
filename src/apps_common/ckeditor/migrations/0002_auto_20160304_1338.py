# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.models
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(max_source_dimensions=(2048, 2048), aspects=(), blank=True, verbose_name='image', variations={'admin_thumbnail': {'crop': False, 'max_width': 250, 'size': (0, 0), 'max_height': 250}, 'mobile': {'crop': False, 'max_width': 512, 'size': (0, 0)}}, upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('simple_photos')),
        ),
    ]
