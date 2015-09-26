# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=libs.stdimage.fields.StdImageField(variations={'admin': {'size': (200, 200), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}, 'small': {'size': (120, 120), 'crop': False}}, min_dimensions=(180, 60), aspects=(), storage=libs.media_storage.MediaStorage('shop/product'), upload_to='', verbose_name='photo'),
            preserve_default=True,
        ),
    ]
