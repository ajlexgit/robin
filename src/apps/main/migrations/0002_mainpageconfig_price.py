# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.valute_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='price',
            field=libs.valute_field.fields.ValuteField(verbose_name='price'),
        ),
    ]
