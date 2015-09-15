# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.fields
import gallery.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150915_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maingalleryvideolinkitem',
            name='preview',
            field=gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath),
            preserve_default=True,
        ),
    ]
