# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='preview2',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(140, 140), storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',), default='', verbose_name='preview', upload_to='', variations={'normal': {'action': 3, 'format': None, 'size': (140, 140)}}),
            preserve_default=False,
        ),
    ]
