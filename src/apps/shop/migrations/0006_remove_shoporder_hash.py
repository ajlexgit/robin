# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150927_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporder',
            name='hash',
        ),
    ]
