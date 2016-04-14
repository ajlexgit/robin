# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.stdimage.fields
import libs.media_storage
import libs.autoslug
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug')),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), min_dimensions=(900, 500), upload_to='', verbose_name='preview', variations={'mobile': {'size': (540, 300)}, 'admin': {'size': (450, 250)}, 'normal': {'size': (900, 500)}}, storage=libs.media_storage.MediaStorage('blog/preview'), blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
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
            field=models.ForeignKey(verbose_name='tag', to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(related_name='posts', through='blog.PostTag', verbose_name='tags', to='blog.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
