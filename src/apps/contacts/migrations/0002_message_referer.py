# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='referer',
            field=models.CharField(blank=True, verbose_name='referer', editable=False, max_length=255),
        ),
    ]
