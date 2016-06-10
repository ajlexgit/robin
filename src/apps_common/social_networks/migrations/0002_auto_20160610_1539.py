# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialpost',
            name='network',
            field=models.CharField(max_length=32, verbose_name='social network', choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], db_index=True, default='facebook'),
        ),
    ]
