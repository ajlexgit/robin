# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galleryitembase',
            options={'verbose_name': 'gallery item', 'verbose_name_plural': 'gallery items', 'default_permissions': (), 'ordering': ('object_id', 'sort_order', 'created')},
        ),
    ]
