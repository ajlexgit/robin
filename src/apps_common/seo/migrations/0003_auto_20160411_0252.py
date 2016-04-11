# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_auto_20160330_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoconfig',
            name='description',
            field=models.TextField(blank=True, max_length=255, verbose_name='site description'),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='description',
            field=models.TextField(blank=True, max_length=255, verbose_name='description'),
        ),
    ]
