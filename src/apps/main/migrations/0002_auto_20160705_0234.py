# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageitem',
            options={'default_permissions': (), 'ordering': ('object_id', 'sort_order', 'created'), 'verbose_name': 'image item', 'verbose_name_plural': 'image items'},
        ),
        migrations.AlterModelOptions(
            name='videoitem',
            options={'default_permissions': (), 'ordering': ('object_id', 'sort_order', 'created'), 'verbose_name': 'video item', 'verbose_name_plural': 'video items'},
        ),
    ]
