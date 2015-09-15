# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import gallery.fields
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_maingalleryvideolinkitem_video_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maingalleryimageitem',
            name='image',
            field=gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, default='', verbose_name='image', storage=libs.media_storage.MediaStorage()),
            preserve_default=False,
        ),
    ]
