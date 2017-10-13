# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('sort_order',), 'default_permissions': ('change',), 'verbose_name': 'Student'},
        ),
        migrations.AddField(
            model_name='student',
            name='sort_order',
            field=models.PositiveIntegerField(verbose_name='order', default=0),
        ),
    ]
