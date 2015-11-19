# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robokassa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='request',
            field=models.TextField(default='', verbose_name='request'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='message',
            field=models.CharField(verbose_name='message', max_length=255),
        ),
    ]
