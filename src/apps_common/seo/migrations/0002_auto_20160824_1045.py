# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoconfig',
            name='title',
            field=models.CharField(max_length=128, verbose_name='meta title', blank=True),
        ),
    ]
