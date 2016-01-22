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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=128, verbose_name='label')),
                ('position', models.CharField(max_length=12, verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(max_length=255, verbose_name='site keywords', blank=True)),
                ('description', models.TextField(max_length=160, verbose_name='site description', blank=True)),
            ],
            options={
                'verbose_name': 'Site config',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128, verbose_name='title', blank=True)),
                ('keywords', models.TextField(max_length=255, verbose_name='keywords', blank=True)),
                ('description', models.TextField(max_length=160, verbose_name='description', blank=True)),
                ('og_title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('og_image', models.ImageField(upload_to='', verbose_name='image', blank=True)),
                ('og_description', models.TextField(verbose_name='description', blank=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
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
