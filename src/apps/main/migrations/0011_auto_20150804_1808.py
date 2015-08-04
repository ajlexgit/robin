# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150804_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='inlinesample',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True),
            preserve_default=True,
        ),
    ]
