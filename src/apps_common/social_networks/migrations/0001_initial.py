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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('network', models.CharField(db_index=True, choices=[('google', 'Google Plus'), ('twitter', 'Twitter'), ('facebook', 'Facebook'), ('linkedin', 'Linked In')], default='facebook', verbose_name='social network', max_length=32)),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.CharField(verbose_name='URL', max_length=512, blank=True)),
                ('image', models.CharField(verbose_name='image URL', max_length=255, blank=True)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified on')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created on')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
            },
        ),
    ]
