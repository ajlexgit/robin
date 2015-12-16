# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemap', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='SitemapConfig',
            old_name='title',
            new_name='header'
        )
    ]
