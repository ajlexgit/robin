# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUsBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'Follow us',
                'verbose_name_plural': 'Follow us',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='SocialConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('facebook', models.URLField(verbose_name='facebook', blank=True)),
                ('twitter', models.URLField(verbose_name='twitter', blank=True)),
                ('youtube', models.URLField(verbose_name='youtube', blank=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
    ]
