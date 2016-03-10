# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='price',
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='preview',
            field=libs.stdimage.fields.StdImageField(blank=True, variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, aspects=('normal',), upload_to='', min_dimensions=(800, 600), verbose_name='preview', storage=libs.media_storage.MediaStorage('main')),
        ),
    ]
