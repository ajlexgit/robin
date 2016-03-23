# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0002_auto_20160323_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('app_name', models.CharField(blank=True, max_length=30, verbose_name='application')),
                ('model_name', models.CharField(blank=True, max_length=30, verbose_name='model')),
                ('instance_id', models.IntegerField(verbose_name='entry id', db_index=True, default=0)),
                ('file', models.FileField(blank=True, verbose_name='file', storage=libs.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.page_file_filename)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'page file',
                'verbose_name_plural': 'page files',
            },
        ),
    ]
