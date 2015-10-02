# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files.models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_listitem_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=150, verbose_name='file', storage=libs.media_storage.MediaStorage(), upload_to=files.models.generate_filepath)),
                ('displayed_name', models.CharField(max_length=150, verbose_name='display name', blank=True, help_text='If you leave it empty the file name will be used')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name_plural': 'files',
                'verbose_name': 'file',
                'ordering': ('sort_order',),
                'abstract': False,
            },
        ),
    ]
