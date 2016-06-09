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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('network', models.CharField(max_length=32, db_index=True, verbose_name='social network', default='facebook', choices=[('google', 'Google Plus'), ('twitter', 'Twitter'), ('facebook', 'Facebook'), ('linkedin', 'Linked In')])),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(verbose_name='sheduled for sharing', default=True)),
                ('created', models.DateTimeField(verbose_name='created on', editable=False, default=django.utils.timezone.now)),
                ('posted', models.DateTimeField(verbose_name='posted on', editable=False, null=True)),
            ],
            options={
                'ordering': ('-scheduled', '-created'),
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
            },
        ),
    ]
