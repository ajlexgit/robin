# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('position', models.CharField(max_length=12, choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], verbose_name='position')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(max_length=255, verbose_name='site keywords', blank=True)),
                ('description', models.TextField(max_length=160, verbose_name='site description', blank=True)),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128, verbose_name='title', blank=True)),
                ('keywords', models.TextField(max_length=255, verbose_name='keywords', blank=True)),
                ('description', models.TextField(max_length=160, verbose_name='description', blank=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'SEO data',
                'verbose_name': 'SEO data',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
