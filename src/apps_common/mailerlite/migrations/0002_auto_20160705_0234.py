# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'default_permissions': ('change',), 'ordering': ('-date_created',), 'verbose_name': 'group', 'verbose_name_plural': 'groups'},
        ),
    ]
