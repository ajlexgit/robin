# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150915_0933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maingalleryvideolinkitem',
            old_name='preview',
            new_name='video_preview',
        ),
    ]
