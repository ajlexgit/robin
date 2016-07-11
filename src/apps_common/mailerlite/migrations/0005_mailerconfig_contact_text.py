# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0004_auto_20160708_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailerconfig',
            name='contact_text',
            field=models.TextField(verbose_name='text', default=''),
            preserve_default=False,
        ),
    ]
