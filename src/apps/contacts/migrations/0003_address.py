# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20160207_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255, blank=True)),
                ('phones', models.CharField(verbose_name='phones', max_length=255, blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(help_text='Double click on the map places marker', verbose_name='coords', blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'ordering': ('sort_order',),
            },
        ),
    ]
