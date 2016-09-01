# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='ajax',
            field=models.BooleanField(help_text='load block through AJAX', verbose_name='AJAX', default=False),
        ),
    ]
