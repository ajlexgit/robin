# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shopconfig_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopproduct',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='create date'),
            preserve_default=True,
        ),
    ]
