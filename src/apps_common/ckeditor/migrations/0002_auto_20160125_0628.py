# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagephoto',
            options={'verbose_name': 'image', 'verbose_name_plural': 'images', 'default_permissions': ('change',)},
        ),
        migrations.AlterModelOptions(
            name='simplephoto',
            options={'verbose_name': 'image', 'verbose_name_plural': 'images', 'default_permissions': ('change',)},
        ),
    ]
