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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(verbose_name='label', max_length=128)),
                ('position', models.CharField(verbose_name='position', max_length=12, choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(verbose_name='site keywords', max_length=255, blank=True)),
                ('description', models.TextField(verbose_name='site description', max_length=160, blank=True)),
            ],
            options={
                'verbose_name': 'Site config',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(verbose_name='title', max_length=128, blank=True)),
                ('keywords', models.TextField(verbose_name='keywords', max_length=255, blank=True)),
                ('description', models.TextField(verbose_name='description', max_length=160, blank=True)),
                ('og_title', models.CharField(verbose_name='title', max_length=255, blank=True)),
                ('og_image', models.ImageField(verbose_name='image', blank=True, upload_to='')),
                ('og_description', models.TextField(verbose_name='description', blank=True)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'SEO data',
                'verbose_name_plural': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
