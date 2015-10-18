# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientformmodel',
            name='image',
            field=libs.stdimage.fields.StdImageField(aspects=('normal',), default='', min_dimensions=(100, 100), storage=libs.media_storage.MediaStorage('main/client_images'), upload_to='', variations={'normal': {'size': (200, 200)}}, verbose_name='image'),
            preserve_default=False,
        ),
    ]
