# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopproduct',
            name='serial',
            field=models.SlugField(verbose_name='serial number', unique=True, max_length=64, help_text='Unique identifier of the product'),
        ),
    ]
