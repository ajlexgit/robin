# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0003_auto_20160719_0707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagefile',
            options={'verbose_name': 'page file', 'default_permissions': (), 'verbose_name_plural': 'page files'},
        ),
        migrations.AlterModelOptions(
            name='pagephoto',
            options={'verbose_name': 'page photo', 'default_permissions': (), 'verbose_name_plural': 'page photos'},
        ),
        migrations.AlterModelOptions(
            name='simplephoto',
            options={'verbose_name': 'simple photo', 'default_permissions': (), 'verbose_name_plural': 'simple photos'},
        ),
    ]
