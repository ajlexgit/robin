# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seodata',
            name='header',
            field=models.CharField(max_length=128, verbose_name='header', blank=True),
            preserve_default=True,
        ),
    ]
