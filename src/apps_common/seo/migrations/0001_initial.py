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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('position', models.CharField(max_length=12, verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(blank=True, verbose_name='site keywords', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='site description', max_length=160)),
            ],
            options={
                'verbose_name': 'Site config',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=128)),
                ('keywords', models.TextField(blank=True, verbose_name='keywords', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='description', max_length=160)),
                ('header', models.CharField(blank=True, verbose_name='header', max_length=128)),
                ('text', models.TextField(blank=True, verbose_name='text')),
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
