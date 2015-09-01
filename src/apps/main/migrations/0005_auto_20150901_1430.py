# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150901_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='header_background',
            field=libs.stdimage.fields.StdImageField(variations={'admin': {'size': (360, 270)}, 'mobile': {'size': (640, 0), 'stretch': False, 'crop': False}, 'desktop': {'size': (1400, 0), 'stretch': False, 'crop': False}}, upload_to='', aspects=(), storage=libs.media_storage.MediaStorage('main/header'), min_dimensions=(1400, 500), default='', verbose_name='background'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='header_video',
            field=models.FileField(upload_to='', blank=True, verbose_name='video'),
            preserve_default=True,
        ),
    ]
