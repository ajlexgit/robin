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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(verbose_name='email', blank=True, max_length=255)),
                ('phone', models.CharField(verbose_name='phone', blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
        ),
    ]
