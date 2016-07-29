# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='title', unique=True)),
                ('description', models.TextField(max_length=1024, verbose_name='short description')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'services',
                'verbose_name': 'service',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='ServicesConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
    ]
