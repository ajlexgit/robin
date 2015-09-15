# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import gallery.models
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150915_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maingalleryvideolinkitem',
            name='preview',
            field=gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='preview', default=''),
            preserve_default=False,
        ),
    ]
