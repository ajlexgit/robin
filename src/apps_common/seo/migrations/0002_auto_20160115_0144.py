# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='SeoData',
            old_name='text_title',
            new_name='header'
        ),
        migrations.RenameField(
            model_name='Counter',
            old_name='title',
            new_name='label'
        ),
    ]
