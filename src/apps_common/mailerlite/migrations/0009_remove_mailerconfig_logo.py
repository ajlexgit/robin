# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0008_auto_20160711_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailerconfig',
            name='logo',
        ),
    ]
