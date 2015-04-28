# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0004_auto_20150428_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seotext',
            name='text',
            field=models.TextField(blank=True, verbose_name='Text'),
            preserve_default=True,
        ),
    ]
