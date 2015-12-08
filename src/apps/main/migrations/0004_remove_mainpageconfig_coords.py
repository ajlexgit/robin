# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151208_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='coords',
        ),
    ]
