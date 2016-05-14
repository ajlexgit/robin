# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='text')),
            ],
            options={
                'managed': False,
                'verbose_name_plural': 'robots.txt',
                'default_permissions': (),
                'verbose_name': 'file',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(max_length=200, unique=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", verbose_name='redirect from')),
                ('new_path', models.CharField(max_length=200, blank=True, help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", verbose_name='redirect to')),
                ('permanent', models.BooleanField(default=True, verbose_name='permanent')),
                ('created', models.DateField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
            ],
            options={
                'verbose_name_plural': 'redirects',
                'ordering': ('old_path',),
                'verbose_name': 'redirect',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(max_length=255, blank=True, verbose_name='site keywords')),
                ('description', models.TextField(max_length=255, blank=True, verbose_name='site description')),
            ],
            options={
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128, blank=True, verbose_name='title')),
                ('keywords', models.TextField(max_length=255, blank=True, verbose_name='keywords')),
                ('description', models.TextField(max_length=255, blank=True, verbose_name='description')),
                ('og_title', models.CharField(max_length=255, blank=True, verbose_name='title')),
                ('og_image', models.ImageField(blank=True, upload_to='', storage=libs.storages.MediaStorage('seo'), verbose_name='image')),
                ('og_description', models.TextField(blank=True, verbose_name='description')),
                ('header', models.CharField(max_length=128, blank=True, verbose_name='header')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'SEO data',
                'verbose_name': 'SEO data',
                'default_permissions': ('change',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
