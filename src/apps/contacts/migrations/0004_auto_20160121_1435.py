# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(verbose_name='date', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(max_length=1536, verbose_name='message'),
        ),
    ]
