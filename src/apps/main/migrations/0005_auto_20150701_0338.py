# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150701_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(verbose_name='icon', default='no_bacterial', size=(30, 30), sprite='img/ev.svg', choices=[('no_bacterial', (-410, 0)), ('no_defence', (-230, 0))]),
            preserve_default=True,
        ),
    ]
