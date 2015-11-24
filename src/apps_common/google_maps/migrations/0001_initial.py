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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('address', models.CharField(verbose_name='address', db_index=True, max_length=255)),
                ('longitude', models.FloatField(verbose_name='longitude')),
                ('latitude', models.FloatField(verbose_name='latitude')),
            ],
        ),
    ]
