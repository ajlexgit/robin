# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.media_storage
import django.utils.timezone
from django.utils.timezone import utc
import libs.stdimage.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='created',
            field=models.DateTimeField(verbose_name='create date', editable=False, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shopcategory',
            name='updated',
            field=models.DateTimeField(verbose_name='change date', auto_now=True, default=datetime.datetime(2015, 11, 2, 18, 38, 27, 727286, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shopproduct',
            name='photo',
            field=libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('shop/product'), aspects=(), verbose_name='photo', upload_to='', min_dimensions=(100, 60), variations={'admin_micro': {'size': (60, 60), 'crop': False, 'background': (255, 255, 255, 255)}, 'admin': {'size': (200, 200), 'crop': False}, 'normal': {'size': (300, 300), 'crop': False}, 'small': {'size': (160, 160), 'crop': False}}),
        ),
    ]
