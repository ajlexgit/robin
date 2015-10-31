# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import libs.valute_field.fields
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientformmodel',
            name='color',
            field=libs.color_field.fields.ColorField(blank=True, verbose_name='color'),
        ),
        migrations.AddField(
            model_name='clientformmodel',
            name='color2',
            field=libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2'),
        ),
        migrations.AddField(
            model_name='clientformmodel',
            name='price',
            field=libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(blank=True, verbose_name='color', choices=[('#FFFFFF', 'white'), ('#FF0000', 'red'), ('#00FF00', 'green'), ('#0000FF', 'blue'), ('#FFFF00', 'yellow'), ('#000000', 'black')]),
        ),
    ]
