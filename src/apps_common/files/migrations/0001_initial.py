# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import files.fields
import files.models
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('file', files.fields.PageFileFileField(upload_to=files.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage('files'), max_length=150, verbose_name='file')),
                ('name', models.CharField(help_text='If you leave it empty the file name will be used', blank=True, verbose_name='name', max_length=150)),
                ('set_name', models.CharField(default='default', max_length=32, verbose_name='set name')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'files',
                'ordering': ('sort_order',),
                'verbose_name': 'file',
            },
        ),
    ]
