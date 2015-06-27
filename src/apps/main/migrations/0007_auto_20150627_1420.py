# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150627_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainpageconfig',
            old_name='coords',
            new_name='ya_coords',
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='go_coords',
            field=google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords'),
            preserve_default=True,
        ),
    ]
