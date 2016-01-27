# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachableblock',
            options={'verbose_name': 'attachable block', 'verbose_name_plural': 'attachable blocks', 'default_permissions': (), 'ordering': ('label',)},
        ),
    ]
