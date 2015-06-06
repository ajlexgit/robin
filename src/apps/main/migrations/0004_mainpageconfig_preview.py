# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150523_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='preview',
            field=libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), min_dimensions=(400, 300), upload_to='', variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, aspects=('normal',), verbose_name='preview', default=''),
            preserve_default=False,
        ),
    ]
