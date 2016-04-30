# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160430_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogconfig',
            name='microdata_author',
            field=models.CharField(verbose_name='author', max_length=255),
        ),
    ]
