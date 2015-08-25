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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
                ('social_facebook', models.URLField(blank=True, max_length=255, verbose_name='facebook')),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
