# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151023_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='preview',
            field=libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',), upload_to='', verbose_name='preview', blank=True, min_dimensions=(400, 300), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}),
        ),
    ]
