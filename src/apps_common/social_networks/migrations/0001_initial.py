# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('network', models.CharField(choices=[('google', 'Google Plus'), ('twitter', 'Twitter'), ('facebook', 'Facebook')], default='facebook', db_index=True, max_length=32, verbose_name='social network')),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('image', models.CharField(max_length=255, blank=True, verbose_name='image URL')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created on', editable=False)),
                ('modified', models.DateTimeField(verbose_name='modified on', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
                'ordering': ('created',),
            },
        ),
    ]
