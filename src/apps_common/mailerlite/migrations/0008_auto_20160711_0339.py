# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0007_auto_20160711_0237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailerconfig',
            name='contact_text',
        ),
        migrations.RemoveField(
            model_name='mailerconfig',
            name='facebook',
        ),
    ]
