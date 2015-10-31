# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151031_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(choices=[('#FFFFFF', 'white'), ('#FF0000', 'red'), ('#00FF00', 'green'), ('#0000FF', 'blue'), ('#FFFF00', 'yellow'), ('#000000', 'black')], verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(verbose_name='color2'),
        ),
    ]
