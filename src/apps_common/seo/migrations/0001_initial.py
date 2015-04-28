# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Site title')),
                ('keywords', models.CharField(max_length=255, blank=True, verbose_name='Site keywords')),
                ('description', models.CharField(max_length=255, blank=True, verbose_name='Site description')),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
    ]
