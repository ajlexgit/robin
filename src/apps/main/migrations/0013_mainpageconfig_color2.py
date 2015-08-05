# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_mainpageconfig_color2'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(default='#FF0000:0.75', verbose_name='color2', blank=True),
            preserve_default=True,
        ),
    ]
