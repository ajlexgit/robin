# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'default_permissions': ('delete',), 'ordering': ('-date',), 'verbose_name': 'message', 'verbose_name_plural': 'messages'},
        ),
    ]
