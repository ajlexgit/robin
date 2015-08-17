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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, verbose_name='email', blank=True)),
                ('phone', models.CharField(max_length=32, verbose_name='phone', blank=True)),
                ('social_facebook', models.URLField(max_length=255, verbose_name='facebook', blank=True)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
