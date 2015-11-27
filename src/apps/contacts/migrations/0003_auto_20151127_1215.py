# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20151124_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactsconfig',
            name='header',
            field=models.CharField(verbose_name='header', max_length=128),
        ),
    ]
