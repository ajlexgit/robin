# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0003_auto_20150924_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachablereference',
            options={'ordering': ('set_name', 'sort_order'), 'verbose_name': 'Attached block', 'verbose_name_plural': 'Attached blocks'},
        ),
        migrations.RenameField(
            model_name='attachablereference',
            old_name='order',
            new_name='sort_order',
        ),
    ]
