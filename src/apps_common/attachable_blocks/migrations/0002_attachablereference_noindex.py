# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachablereference',
            name='noindex',
            field=models.BooleanField(verbose_name='SEO indexation', default=True, help_text='wraps block with <!--noidex-->'),
        ),
    ]
