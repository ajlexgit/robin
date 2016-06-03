# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='title', unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='title', unique=True),
        ),
    ]
