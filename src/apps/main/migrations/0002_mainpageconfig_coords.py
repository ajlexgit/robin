# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords',
            field=google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True),
        ),
    ]
