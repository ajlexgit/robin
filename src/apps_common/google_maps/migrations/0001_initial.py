# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapAndAddress',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=255, db_index=True, verbose_name='address')),
                ('longitude', models.FloatField(verbose_name='longitude')),
                ('latitude', models.FloatField(verbose_name='latitude')),
            ],
        ),
    ]
