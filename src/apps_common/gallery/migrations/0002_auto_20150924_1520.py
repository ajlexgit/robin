# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galleryitembase',
            options={'verbose_name_plural': 'gallery items', 'ordering': ('object_id', 'sort_order', 'created'), 'verbose_name': 'gallery item'},
        ),
        migrations.RenameField(
            model_name='galleryitembase',
            old_name='order',
            new_name='sort_order',
        ),
    ]
