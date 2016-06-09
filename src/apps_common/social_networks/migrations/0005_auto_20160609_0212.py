# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0004_auto_20160609_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialpost',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
    ]
