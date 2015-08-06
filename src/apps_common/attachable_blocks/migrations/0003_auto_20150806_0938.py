# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_auto_20150806_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachableblock',
            name='block_model',
            field=models.CharField(verbose_name='block model', choices=[('main.models.MainBlockFirst', 'First block type'), ('main.models.MainBlockSecond', 'Second block type')], max_length=255, editable=False),
            preserve_default=True,
        ),
    ]
