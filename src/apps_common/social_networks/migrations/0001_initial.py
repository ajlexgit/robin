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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('network', models.CharField(verbose_name='social network', default='facebook', max_length=32, choices=[('google', 'Google Plus'), ('twitter', 'Twitter'), ('facebook', 'Facebook'), ('linkedin', 'Linked In')], db_index=True)),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.CharField(verbose_name='URL', max_length=512, blank=True)),
                ('image', models.CharField(verbose_name='image URL', max_length=255, blank=True)),
                ('created', models.DateTimeField(verbose_name='created on', default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(verbose_name='modified on', auto_now=True)),
            ],
            options={
                'verbose_name': 'post',
                'ordering': ('-created',),
                'verbose_name_plural': 'posts',
            },
        ),
    ]
