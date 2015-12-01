# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
                ('facebook', models.URLField(blank=True, verbose_name='facebook')),
                ('twitter', models.URLField(blank=True, verbose_name='twitter')),
                ('youtube', models.URLField(blank=True, verbose_name='youtube')),
            ],
            options={
                'verbose_name': 'Social network',
            },
        ),
    ]
