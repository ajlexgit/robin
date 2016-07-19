# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import ckeditor.fields
import libs.autoslug
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('microdata_author', models.CharField(verbose_name='author', max_length=255)),
                ('microdata_publisher_logo', models.ImageField(verbose_name='logo', storage=libs.storages.media_storage.MediaStorage('microdata'), upload_to='')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', unique=True, populate_from='header')),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('status', models.IntegerField(verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')], default=1)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage('blog/preview'), blank=True, variations={'admin': {'size': (450, 250)}, 'normal': {'size': (900, 500)}, 'mobile': {'size': (540, 300)}}, min_dimensions=(900, 500), aspects=('normal',), upload_to='')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Post',
                'ordering': ('-date', '-id'),
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('post', models.ForeignKey(verbose_name='post', to='blog.BlogPost')),
            ],
            options={
                'verbose_name': 'post tag',
                'verbose_name_plural': 'post tags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', unique=True, populate_from='title')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='posttag',
            name='tag',
            field=models.ForeignKey(verbose_name='tag', to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(verbose_name='tags', to='blog.Tag', through='blog.PostTag', related_name='posts'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
