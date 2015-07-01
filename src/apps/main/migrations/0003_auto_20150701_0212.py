# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150628_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(verbose_name='icon', choices=[('icon 1', (10, 10)), ('icon 2', (50, 50))], default='', sprite='img/ev.svg'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', blank=True, default=''),
            preserve_default=False,
        ),
    ]
