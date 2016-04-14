# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.TextField(verbose_name='text', blank=True)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'robots.txt',
                'managed': False,
                'verbose_name': 'file',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(verbose_name='label', max_length=128)),
                ('position', models.CharField(verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], max_length=12)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(max_length=255, verbose_name='site keywords', blank=True)),
                ('description', models.TextField(max_length=255, verbose_name='site description', blank=True)),
            ],
            options={
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128, verbose_name='title', blank=True)),
                ('keywords', models.TextField(max_length=255, verbose_name='keywords', blank=True)),
                ('description', models.TextField(max_length=255, verbose_name='description', blank=True)),
                ('og_title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('og_image', models.ImageField(upload_to='', verbose_name='image', storage=libs.media_storage.MediaStorage('seo'), blank=True)),
                ('og_description', models.TextField(verbose_name='description', blank=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
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
