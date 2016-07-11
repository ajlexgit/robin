# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0006_mailerconfig_footer_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailerconfig',
            name='company',
        ),
        migrations.AddField(
            model_name='mailerconfig',
            name='facebook',
            field=models.URLField(blank=True, verbose_name='facebook'),
        ),
    ]
