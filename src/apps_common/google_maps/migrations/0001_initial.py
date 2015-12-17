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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('address', models.CharField(max_length=255, db_index=True, verbose_name='address')),
                ('longitude', models.FloatField(verbose_name='longitude')),
                ('latitude', models.FloatField(verbose_name='latitude')),
            ],
        ),
    ]
