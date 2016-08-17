# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags', 'ordering': ('sort_order',)},
        ),
        migrations.AddField(
            model_name='tag',
            name='sort_order',
            field=models.IntegerField(verbose_name='order', default=0),
        ),
    ]
