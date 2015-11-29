# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
            ],
            options={
                'verbose_name': 'Configuration',
            },
        ),
    ]
