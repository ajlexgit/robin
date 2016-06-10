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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('network', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')], db_index=True, default='facebook', max_length=32, verbose_name='social network')),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(default=True, verbose_name='sheduled for sharing')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
                ('posted', models.DateTimeField(null=True, editable=False, verbose_name='posted on')),
            ],
            options={
                'verbose_name_plural': 'posts',
                'ordering': ('-scheduled', '-created'),
                'verbose_name': 'post',
            },
        ),
    ]
