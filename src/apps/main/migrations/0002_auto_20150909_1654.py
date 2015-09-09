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
        migrations.AlterField(
            model_name='mainpageconfig',
            name='header_background',
            field=libs.stdimage.fields.StdImageField(variations={'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}, 'admin': {'size': (360, 270)}}, upload_to='', verbose_name='background', storage=libs.media_storage.MediaStorage('main/header'), min_dimensions=(1024, 500), aspects=()),
            preserve_default=True,
        ),
    ]
