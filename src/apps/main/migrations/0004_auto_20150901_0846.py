# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150826_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='preview2',
            field=libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', aspects=('normal',), min_dimensions=(100, 100), variations={'normal': {'size': (200, 200)}}),
            preserve_default=True,
        ),
    ]
