# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import ckeditor.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(960, 540), variations={'admin_thumbnail': {'size': (224, 126)}, 'mobile': {'size': (512, 288)}, 'wide': {'size': (1440, 810)}, 'normal': {'size': (960, 540)}}, blank=True, upload_to=ckeditor.models.page_photo_filename, storage=libs.media_storage.MediaStorage('page_photos'), verbose_name='image', aspects='on_page'),
        ),
    ]
