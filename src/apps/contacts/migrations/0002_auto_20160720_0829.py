# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='phones',
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(verbose_name='phone', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.CharField(verbose_name='region', max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(verbose_name='zip', max_length=32, blank=True),
        ),
    ]
