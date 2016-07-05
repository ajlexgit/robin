# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posttag',
            options={'verbose_name': 'post tag', 'verbose_name_plural': 'post tags'},
        ),
    ]
