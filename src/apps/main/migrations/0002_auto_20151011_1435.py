# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', max_length=14, blank=True),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(verbose_name='color2', max_length=14, blank=True),
        ),
    ]
