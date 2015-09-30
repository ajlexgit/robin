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
        migrations.AddField(
            model_name='shopcategory',
            name='product_count',
            field=models.PositiveIntegerField(editable=False, default=0, help_text='count of visible products'),
        ),
        migrations.AlterField(
            model_name='shopproduct',
            name='photo',
            field=libs.stdimage.fields.StdImageField(aspects=(), min_dimensions=(180, 60), storage=libs.media_storage.MediaStorage('shop/product'), upload_to='', variations={'admin_micro': {'background': (255, 255, 255, 255), 'size': (60, 60), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}, 'admin': {'size': (200, 200), 'crop': False}, 'small': {'size': (160, 160), 'crop': False}}, verbose_name='photo'),
        ),
    ]
