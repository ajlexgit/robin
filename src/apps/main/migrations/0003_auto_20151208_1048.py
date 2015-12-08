# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import google_maps.fields
import libs.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mainpageconfig_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords',
            field=google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coordinates', null=True),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='preview',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(800, 600), blank=True, verbose_name='preview', variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, storage=libs.media_storage.MediaStorage('main'), upload_to='', aspects=('normal',)),
        ),
    ]
