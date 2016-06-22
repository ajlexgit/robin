# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import django.utils.timezone
import ckeditor.fields
import libs.autoslug


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
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='header', unique=True)),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('status', models.IntegerField(verbose_name='status', default=1, choices=[(1, 'Draft'), (2, 'Public')])),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage('blog/preview'), upload_to='', min_dimensions=(900, 500), blank=True, variations={'normal': {'size': (900, 500)}, 'mobile': {'size': (540, 300)}, 'admin': {'size': (450, 250)}}, aspects=('normal',))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-date', '-id'),
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('post', models.ForeignKey(verbose_name='post', to='blog.BlogPost')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='title', unique=True)),
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
            field=models.ManyToManyField(verbose_name='tags', related_name='posts', to='blog.Tag', through='blog.PostTag'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
