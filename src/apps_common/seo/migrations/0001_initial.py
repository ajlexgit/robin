# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, verbose_name='text')),
            ],
            options={
                'verbose_name_plural': 'robots.txt',
                'verbose_name': 'file',
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128, verbose_name='label')),
                ('position', models.CharField(max_length=12, verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('old_path', models.CharField(max_length=200, verbose_name='redirect from', help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", unique=True)),
                ('new_path', models.CharField(blank=True, max_length=200, verbose_name='redirect to', help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.")),
                ('permanent', models.BooleanField(default=True, verbose_name='permanent')),
                ('created', models.DateField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
            ],
            options={
                'verbose_name_plural': 'redirects',
                'verbose_name': 'redirect',
                'ordering': ('old_path',),
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='site title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='site keywords')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='site description')),
            ],
            options={
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='keywords')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='description')),
                ('canonical', models.URLField(blank=True, verbose_name='canonical URL')),
                ('og_title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('og_image', models.ImageField(blank=True, verbose_name='image', upload_to='', storage=libs.storages.media_storage.MediaStorage('seo'))),
                ('og_description', models.TextField(blank=True, verbose_name='description')),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
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
