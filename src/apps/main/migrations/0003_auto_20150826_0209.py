# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150826_0144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientinlineformmodel',
            options={},
        ),
        migrations.RemoveField(
            model_name='clientinlineformmodel',
            name='order',
        ),
    ]
