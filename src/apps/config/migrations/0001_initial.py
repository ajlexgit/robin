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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('email', models.EmailField(verbose_name='email', blank=True, max_length=255)),
                ('phone', models.CharField(verbose_name='phone', blank=True, max_length=32)),
                ('social_facebook', models.URLField(verbose_name='facebook', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
