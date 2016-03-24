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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('label', models.CharField(max_length=128, verbose_name='label')),
                ('position', models.CharField(choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], max_length=12, verbose_name='position')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='site keywords')),
                ('description', models.TextField(blank=True, max_length=160, verbose_name='site description')),
            ],
            options={
                'verbose_name': 'Site config',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='keywords')),
                ('description', models.TextField(blank=True, max_length=160, verbose_name='description')),
                ('og_title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('og_image', models.ImageField(blank=True, upload_to='', verbose_name='image')),
                ('og_description', models.TextField(blank=True, verbose_name='description')),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name_plural': 'SEO data',
                'verbose_name': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
