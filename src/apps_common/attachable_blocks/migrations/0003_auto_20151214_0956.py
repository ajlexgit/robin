# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_attachablereference_noindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='noindex',
            field=models.BooleanField(verbose_name='NoIndex', default=True, help_text='wraps block with &lt;!--noidex--&gt;'),
        ),
    ]
