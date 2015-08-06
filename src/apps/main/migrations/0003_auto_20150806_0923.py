# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150806_0823'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mainpageblockref',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='mainpageblockref',
            name='block',
        ),
        migrations.RemoveField(
            model_name='mainpageblockref',
            name='page',
        ),
        migrations.AlterModelOptions(
            name='mainblockfirst',
            options={'verbose_name_plural': 'First blocks'},
        ),
        migrations.AlterModelOptions(
            name='mainblocksecond',
            options={'verbose_name_plural': 'Second blocks'},
        ),
        migrations.RemoveField(
            model_name='mainpageconfig',
            name='blocks',
        ),
        migrations.DeleteModel(
            name='MainPageBlockRef',
        ),
    ]
