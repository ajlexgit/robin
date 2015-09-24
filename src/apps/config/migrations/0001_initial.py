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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email', blank=True)),
                ('phone', models.CharField(max_length=32, verbose_name='phone', blank=True)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
