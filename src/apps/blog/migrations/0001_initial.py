# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.autoslug
import django.utils.timezone
import ckeditor.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('microdata_author', models.CharField(max_length=255, verbose_name='author')),
                ('microdata_publisher_logo', models.ImageField(upload_to='', storage=libs.storages.media_storage.MediaStorage('microdata'), verbose_name='logo')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='header', verbose_name='slug', unique=True)),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Public')], default=1, verbose_name='status')),
                ('preview', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(900, 500), blank=True, verbose_name='preview', variations={'admin': {'size': (450, 250)}, 'mobile': {'size': (540, 300)}, 'normal': {'size': (900, 500)}}, storage=libs.storages.media_storage.MediaStorage('blog/preview'), aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'ordering': ('-date', '-id'),
                'verbose_name_plural': 'Posts',
                'verbose_name': 'Post',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(to='blog.BlogPost', verbose_name='post')),
            ],
            options={
                'verbose_name_plural': 'post tags',
                'verbose_name': 'post tag',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug', unique=True)),
                ('sort_order', models.IntegerField(default=0, verbose_name='order')),
            ],
            options={
                'ordering': ('sort_order',),
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
            field=models.ManyToManyField(through='blog.PostTag', to='blog.Tag', related_name='posts', verbose_name='tags'),
        ),
        migrations.AlterUniqueTogether(
            name='posttag',
            unique_together=set([('post', 'tag')]),
        ),
    ]
