# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150517_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='coords2',
            field=google_maps.fields.GoogleCoordsField(verbose_name='координаты', null=True, blank=True),
            preserve_default=True,
        ),
    ]
