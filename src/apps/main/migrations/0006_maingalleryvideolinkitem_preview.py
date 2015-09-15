# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import gallery.models
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_maingalleryvideolinkitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='maingalleryvideolinkitem',
            name='preview',
            field=gallery.fields.GalleryImageField(verbose_name='preview', null=True, upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), blank=True),
            preserve_default=True,
        ),
    ]
