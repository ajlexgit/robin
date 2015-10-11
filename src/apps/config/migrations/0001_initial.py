# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255, blank=True, verbose_name='email')),
                ('phone', models.CharField(max_length=32, blank=True, verbose_name='phone')),
            ],
            options={
                'verbose_name': 'Configuration',
            },
        ),
    ]
