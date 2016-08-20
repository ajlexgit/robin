# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
            ],
            options={
                'verbose_name': 'file',
                'default_permissions': (),
                'managed': False,
                'verbose_name_plural': 'robots.txt',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('label', models.CharField(verbose_name='label', max_length=128)),
                ('position', models.CharField(verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], max_length=12)),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'counter',
                'verbose_name_plural': 'counters',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('old_path', models.CharField(verbose_name='redirect from', help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, unique=True)),
                ('new_path', models.CharField(verbose_name='redirect to', blank=True, help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200)),
                ('permanent', models.BooleanField(verbose_name='permanent', default=True)),
                ('note', models.TextField(verbose_name='note', blank=True, max_length=255)),
                ('created', models.DateField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'redirect',
                'ordering': ('old_path',),
                'verbose_name_plural': 'redirects',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='meta title', max_length=128)),
                ('keywords', models.TextField(verbose_name='meta keywords', blank=True, max_length=255)),
                ('description', models.TextField(verbose_name='meta description', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Defaults',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(verbose_name='meta title', blank=True, max_length=128)),
                ('keywords', models.TextField(verbose_name='meta keywords', blank=True, max_length=255)),
                ('description', models.TextField(verbose_name='meta description', blank=True, max_length=255)),
                ('canonical', models.URLField(verbose_name='canonical URL', blank=True)),
                ('og_title', models.CharField(verbose_name='title', blank=True, max_length=255)),
                ('og_image', models.ImageField(verbose_name='image', upload_to='', storage=libs.storages.media_storage.MediaStorage('seo'), blank=True)),
                ('og_description', models.TextField(verbose_name='description', blank=True)),
                ('header', models.CharField(verbose_name='header', blank=True, max_length=128)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'SEO data',
                'default_permissions': ('change',),
                'verbose_name_plural': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
