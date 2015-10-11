# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151011_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', blank=True),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='video',
            field=libs.videolink_field.fields.VideoLinkField(providers=set(['youtube']), verbose_name='video', blank=True),
        ),
    ]
