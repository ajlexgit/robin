# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20150804_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inlinesample',
            name='color',
            field=libs.color_field.fields.ColorOpacityField(verbose_name='color'),
            preserve_default=True,
        ),
    ]
