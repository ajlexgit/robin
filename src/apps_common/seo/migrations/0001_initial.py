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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('position', models.CharField(choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], max_length=12, verbose_name='position')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'counter',
                'verbose_name_plural': 'counters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(verbose_name='site keywords', blank=True, max_length=255)),
                ('description', models.TextField(verbose_name='site description', blank=True, max_length=160)),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
