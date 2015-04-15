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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='Site title', max_length=64)),
                ('keywords', models.CharField(blank=True, verbose_name='Site keywords', max_length=255)),
                ('description', models.CharField(blank=True, verbose_name='Site description', max_length=255)),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
    ]
