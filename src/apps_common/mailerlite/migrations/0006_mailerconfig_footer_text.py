# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0005_mailerconfig_contact_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailerconfig',
            name='footer_text',
            field=models.TextField(verbose_name='text', blank=True),
        ),
    ]
