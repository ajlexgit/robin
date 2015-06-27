# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150615_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='color',
            field=libs.color_field.fields.ColorField(verbose_name='color', default=''),
            preserve_default=False,
        ),
    ]
