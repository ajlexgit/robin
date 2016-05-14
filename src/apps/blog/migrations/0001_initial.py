# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import django.utils.timezone
import libs.autoslug
import libs.media_storage
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('microdata_author', models.CharField(max_length=255, verbose_name='author')),
                ('microdata_publisher_logo', models.ImageField(storage=libs.media_storage.MediaStorage('microdata'), upload_to='', verbose_name='logo')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug')),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Public')], default=1, verbose_name='status')),
                ('preview', libs.stdimage.fields.StdImageField(min_dimensions=(900, 500), variations={'admin': {'size': (450, 250)}, 'mobile': {'size': (540, 300)}, 'normal': {'size': (900, 500)}}, storage=libs.media_storage.MediaStorage('blog/preview'), upload_to='', verbose_name='preview', blank=True, aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'ordering': ('-date', '-id'),
                'verbose_name': 'Post',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(to='blog.BlogPost', verbose_name='post')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='posttag',
            name='tag',
            field=models.ForeignKey(to='blog.Tag', verbose_name='tag'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.Tag', through='blog.PostTag', verbose_name='tags'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
