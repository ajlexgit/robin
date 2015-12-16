# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemap', '0002_auto_20151215_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemapconfig',
            name='header',
            field=models.CharField(max_length=255, verbose_name='header'),
        ),
    ]
