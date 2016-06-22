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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'robots.txt',
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('old_path', models.CharField(verbose_name='redirect from', help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, unique=True)),
                ('new_path', models.CharField(verbose_name='redirect to', help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200, blank=True)),
                ('permanent', models.BooleanField(verbose_name='permanent', default=True)),
                ('note', models.TextField(verbose_name='note', max_length=255, blank=True)),
                ('created', models.DateField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
                'ordering': ('old_path',),
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='site title', max_length=128)),
                ('keywords', models.TextField(verbose_name='site keywords', max_length=255, blank=True)),
                ('description', models.TextField(verbose_name='site description', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(verbose_name='title', max_length=128, blank=True)),
                ('keywords', models.TextField(verbose_name='keywords', max_length=255, blank=True)),
                ('description', models.TextField(verbose_name='description', max_length=255, blank=True)),
                ('canonical', models.URLField(verbose_name='canonical URL', blank=True)),
                ('og_title', models.CharField(verbose_name='title', max_length=255, blank=True)),
                ('og_image', models.ImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage('seo'), upload_to='', blank=True)),
                ('og_description', models.TextField(verbose_name='description', blank=True)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'SEO data',
                'verbose_name_plural': 'SEO data',
                'default_permissions': ('change',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
