# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapAndAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('address', models.CharField(max_length=255, verbose_name='address', db_index=True)),
                ('longitude', models.FloatField(verbose_name='longitude')),
                ('latitude', models.FloatField(verbose_name='latitude')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
