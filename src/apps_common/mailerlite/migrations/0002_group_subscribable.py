# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='subscribable',
            field=models.BooleanField(default=False, verbose_name='subscribable'),
        ),
    ]
