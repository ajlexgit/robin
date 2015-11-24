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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(verbose_name='email', blank=True, max_length=255)),
                ('phone', models.CharField(verbose_name='phone', blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
        ),
    ]
