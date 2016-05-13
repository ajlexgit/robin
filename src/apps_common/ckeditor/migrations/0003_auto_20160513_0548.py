# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import ckeditor.models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0002_auto_20160504_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(aspects=(), storage=libs.media_storage.MediaStorage('simple_photos'), variations={'mobile': {'max_width': 512, 'size': (0, 0), 'crop': False}}, blank=True, max_source_dimensions=(3072, 3072), upload_to=ckeditor.models.page_photo_filename, verbose_name='image'),
        ),
    ]
