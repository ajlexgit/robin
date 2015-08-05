# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_mainpageconfig_color2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2'),
            preserve_default=True,
        ),
    ]
