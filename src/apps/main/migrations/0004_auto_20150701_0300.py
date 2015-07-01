# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150701_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpageconfig',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(default='no_bacterial', sprite='img/ev.svg', verbose_name='icon', choices=[('no_bacterial', (-410, 0)), ('no_defence', (-230, 0))]),
            preserve_default=True,
        ),
    ]
