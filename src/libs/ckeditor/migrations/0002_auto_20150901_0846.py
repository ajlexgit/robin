# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage
import libs.ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(verbose_name='image', storage=libs.media_storage.MediaStorage('simple_photos'), upload_to=libs.ckeditor.models.page_photo_filename, max_source_dimensions=(1024, 1024), aspects=(), variations={'admin_thumbnail': {'size': (150, 85), 'crop': False, 'stretch': False}}, blank=True),
            preserve_default=True,
        ),
    ]
