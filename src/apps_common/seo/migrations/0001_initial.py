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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='text')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128, verbose_name='label')),
                ('position', models.CharField(db_index=True, max_length=12, verbose_name='position', choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
                ('content', models.TextField(verbose_name='content')),
                ('sort_order', models.IntegerField(default=0, verbose_name='order')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name_plural': 'counters',
                'verbose_name': 'counter',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200, verbose_name='redirect from', unique=True)),
                ('new_path', models.CharField(blank=True, max_length=200, verbose_name='redirect to', help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.")),
                ('permanent', models.BooleanField(default=True, verbose_name='permanent')),
                ('note', models.TextField(blank=True, max_length=255, verbose_name='note')),
                ('created', models.DateField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('last_usage', models.DateField(editable=False, null=True, verbose_name='last usage')),
            ],
            options={
                'ordering': ('old_path',),
                'verbose_name_plural': 'redirects',
                'verbose_name': 'redirect',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='meta title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='meta keywords')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='meta description')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='meta title')),
                ('keywords', models.TextField(blank=True, max_length=255, verbose_name='meta keywords')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='meta description')),
                ('canonical', models.URLField(blank=True, verbose_name='canonical URL')),
                ('noindex', models.BooleanField(help_text='text on the page will not be indexed', default=False, verbose_name='noindex')),
                ('og_title', models.CharField(blank=True, max_length=255, verbose_name='header')),
                ('og_image', models.ImageField(blank=True, upload_to='', verbose_name='image', storage=libs.storages.media_storage.MediaStorage('seo'))),
                ('og_description', models.TextField(blank=True, verbose_name='description')),
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
