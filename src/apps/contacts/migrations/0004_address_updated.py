# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20160425_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='change date', default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
