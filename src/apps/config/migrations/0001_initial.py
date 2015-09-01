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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('email', models.EmailField(verbose_name='email', max_length=255, blank=True)),
                ('phone', models.CharField(verbose_name='phone', max_length=32, blank=True)),
                ('social_facebook', models.URLField(verbose_name='facebook', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
