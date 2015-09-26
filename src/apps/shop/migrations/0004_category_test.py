# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150925_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='test',
            field=models.FileField(blank=True, upload_to='', verbose_name='test'),
            preserve_default=True,
        ),
    ]
