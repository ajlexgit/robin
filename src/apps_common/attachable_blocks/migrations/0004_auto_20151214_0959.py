# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0003_auto_20151214_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachablereference',
            name='ajax',
            field=models.BooleanField(default=False, help_text='load block with AJAX', verbose_name='AJAX load'),
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='noindex',
            field=models.BooleanField(default=True, help_text='wraps block with &lt;!--noidex--&gt;', verbose_name='noIndex'),
        ),
    ]
