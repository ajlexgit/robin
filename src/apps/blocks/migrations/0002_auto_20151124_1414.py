# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sampleblock',
            options={'verbose_name': 'sample block', 'verbose_name_plural': 'sample blocks'},
        ),
    ]
