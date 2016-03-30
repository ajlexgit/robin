# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(aspects='normal', upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('page_photos'), min_dimensions=(960, 540), variations={'admin_thumbnail': {'size': (224, 126)}, 'wide': {'size': (1440, 810)}, 'mobile': {'size': (512, 288)}, 'normal': {'size': (960, 540)}}, verbose_name='image', blank=True),
        ),
    ]
