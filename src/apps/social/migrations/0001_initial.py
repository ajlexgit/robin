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
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', parent_link=True, auto_created=True, primary_key=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
                ('facebook', models.URLField(verbose_name='facebook', blank=True)),
                ('twitter', models.URLField(verbose_name='twitter', blank=True)),
                ('youtube', models.URLField(verbose_name='youtube', blank=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
    ]
