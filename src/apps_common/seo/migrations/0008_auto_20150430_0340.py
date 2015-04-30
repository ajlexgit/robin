# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0007_auto_20150430_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seodata',
            name='title',
            field=models.CharField(blank=True, verbose_name='title', max_length=128),
            preserve_default=True,
        ),
    ]
