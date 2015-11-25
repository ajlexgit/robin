# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date'),
        ),
    ]
