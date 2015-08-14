# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0007_attachableblockref_frame'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachableblockref',
            options={'verbose_name_plural': 'Block references', 'verbose_name': 'Block reference', 'ordering': ('frame', 'order')},
        ),
    ]
