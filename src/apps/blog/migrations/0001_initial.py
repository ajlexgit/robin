# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.stdimage.fields
import libs.autoslug
import django.utils.timezone
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from=('title',))),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('status', models.IntegerField(verbose_name='status', default=1, choices=[(1, 'Draft'), (2, 'Public')])),
                ('preview', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(900, 500), storage=libs.media_storage.MediaStorage('blog/preview'), variations={'mobile': {'size': (540, 300)}, 'admin': {'size': (450, 250)}, 'normal': {'size': (900, 500)}}, verbose_name='preview', aspects=('normal',), blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from=('title',))),
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
            field=models.ManyToManyField(verbose_name='tags', related_name='posts', through='blog.PostTag', to='blog.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
