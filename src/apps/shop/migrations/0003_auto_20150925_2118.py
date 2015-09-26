# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150925_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo_crop',
            field=models.CharField(editable=False, verbose_name='crop area', default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), variations={'admin': {'size': (200, 200), 'crop': False}, 'admin_micro': {'background': (255, 255, 255, 255), 'size': (50, 50), 'crop': False}, 'small': {'size': (120, 120), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}}, aspects=(), min_dimensions=(180, 60), upload_to='', verbose_name='photo'),
            preserve_default=True,
        ),
    ]
