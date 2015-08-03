# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.valute_field.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150702_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='price',
            field=libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
