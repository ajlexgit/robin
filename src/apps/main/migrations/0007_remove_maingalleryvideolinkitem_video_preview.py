# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_maingalleryvideolinkitem_preview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maingalleryvideolinkitem',
            name='video_preview',
        ),
    ]
