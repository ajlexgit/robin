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
                ('email', models.EmailField(blank=True, verbose_name='email', max_length=255)),
                ('phone', models.CharField(blank=True, verbose_name='phone', max_length=32)),
            ],
            options={
                'verbose_name': 'Configuration',
            },
            bases=(models.Model,),
        ),
    ]
