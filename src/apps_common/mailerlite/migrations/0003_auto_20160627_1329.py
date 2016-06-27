# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0002_auto_20160627_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='header_image',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(640, 150), storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), variations={'admin': {'size': (480, 90)}, 'normal': {'quality': 95, 'size': (640, 150)}}, blank=True, aspects='normal', upload_to='', verbose_name='preview'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(verbose_name='text'),
        ),
    ]
