# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160603_0420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='title',
            new_name='header',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=libs.autoslug.AutoSlugField(verbose_name='slug', unique=True, populate_from='header'),
        ),
    ]
