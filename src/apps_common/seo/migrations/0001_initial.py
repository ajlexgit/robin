# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('label', models.CharField(verbose_name='label', max_length=128)),
                ('position', models.CharField(choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], verbose_name='position', max_length=12)),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'counter',
                'verbose_name_plural': 'counters',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(verbose_name='site keywords', blank=True, max_length=255)),
                ('description', models.TextField(verbose_name='site description', blank=True, max_length=160)),
            ],
            options={
                'verbose_name': 'Site config',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(verbose_name='title', blank=True, max_length=128)),
                ('keywords', models.TextField(verbose_name='keywords', blank=True, max_length=255)),
                ('description', models.TextField(verbose_name='description', blank=True, max_length=160)),
                ('header', models.CharField(verbose_name='header', blank=True, max_length=128)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'SEO data',
                'verbose_name_plural': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
