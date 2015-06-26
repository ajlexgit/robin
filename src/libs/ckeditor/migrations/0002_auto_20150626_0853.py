# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields
import libs.ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(aspects=(), max_source_dimensions=(1024, 1024), storage=libs.media_storage.MediaStorage('simple_photos'), variations={'admin_thumbnail': {'action': 3, 'size': (150, 85)}}, verbose_name='image', upload_to=libs.ckeditor.models.page_photo_filename, blank=True),
            preserve_default=True,
        ),
    ]
