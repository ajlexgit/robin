# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.storages.media_storage
import libs.stdimage.fields
import django.utils.timezone
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('microdata_author', models.CharField(max_length=255, verbose_name='author')),
                ('microdata_publisher_logo', models.ImageField(verbose_name='logo', upload_to='', storage=libs.storages.media_storage.MediaStorage('microdata'))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='header', unique=True)),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(900, 500), storage=libs.storages.media_storage.MediaStorage('blog/preview'), blank=True, variations={'admin': {'size': (450, 250)}, 'mobile': {'size': (540, 300)}, 'normal': {'size': (900, 500)}}, upload_to='', aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'verbose_name': 'Post',
                'ordering': ('-date', '-id'),
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('post', models.ForeignKey(verbose_name='post', to='blog.BlogPost')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(verbose_name='slug', populate_from='title', unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
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
            field=models.ManyToManyField(through='blog.PostTag', verbose_name='tags', related_name='posts', to='blog.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
