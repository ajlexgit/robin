# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='note',
            field=models.TextField(verbose_name='note', max_length=255, blank=True),
        ),
    ]
