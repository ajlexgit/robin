# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mainpageconfig_preview2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='preview2',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(100, 100), storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', aspects=('normal',), variations={'normal': {'action': 3, 'size': (140, 140)}}, verbose_name='preview'),
            preserve_default=True,
        ),
    ]
