# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128, verbose_name='label')),
                ('position', models.CharField(max_length=12, choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], verbose_name='position')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(max_length=255, blank=True, verbose_name='site keywords')),
                ('description', models.TextField(max_length=160, blank=True, verbose_name='site description')),
            ],
            options={
                'verbose_name': 'Site config',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128, blank=True, verbose_name='title')),
                ('keywords', models.TextField(max_length=255, blank=True, verbose_name='keywords')),
                ('description', models.TextField(max_length=160, blank=True, verbose_name='description')),
                ('header', models.CharField(max_length=128, blank=True, verbose_name='header')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'SEO data',
                'verbose_name': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
