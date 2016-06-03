# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160603_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='header',
            field=models.CharField(max_length=255, verbose_name='header'),
        ),
    ]
