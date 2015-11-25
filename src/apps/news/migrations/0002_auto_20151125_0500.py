# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts', 'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(verbose_name='create date', default=django.utils.timezone.now, editable=False),
        ),
    ]
