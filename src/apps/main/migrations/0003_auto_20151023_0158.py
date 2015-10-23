# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models
import gallery.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_clientformmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maingalleryvideolinkitem',
            name='video_preview',
            field=gallery.fields.GalleryVideoLinkPreviewField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='preview', blank=True),
        ),
    ]
