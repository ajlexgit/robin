# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import libs.checks
import gallery.fields
import files.fields
import django.db.models.deletion
import libs.autoslug
import posts.models
import gallery.models
import libs.stdimage.fields
import libs.ckeditor.fields
import datetime
import libs.media_storage
import files.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from='title', unique=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', variations={'big': {'action': 3, 'watermark': {'padding': (20, 20), 'opacity': 0.6, 'file': 'img/watermark.png'}, 'size': (800, 600)}, 'normal': {'size': (280, 200)}, 'small': {'size': (140, 100)}}, upload_to=posts.models.post_preview_filename, blank=True, aspects='normal', storage=libs.media_storage.MediaStorage('posts/preview'), min_dimensions=(280, 200))),
                ('note', libs.ckeditor.fields.CKEditorField(verbose_name='note')),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='date')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', files.fields.RemovableFileField(verbose_name='file', storage=libs.media_storage.MediaStorage(), upload_to=files.models.generate_filepath, max_length=150)),
                ('displayed_name', models.CharField(verbose_name='display name', blank=True, help_text='If you leave it empty the file name will be used', max_length=150)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order', blank=True)),
                ('post', models.ForeignKey(verbose_name='post', related_name='files', to='posts.Post')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, blank=True, null=True, storage=libs.media_storage.MediaStorage())),
                ('crop', models.CharField(verbose_name='image crop coordinates', max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='PostGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='gallery.GalleryItemBase')),
                ('video_provider', models.PositiveSmallIntegerField(default=0, verbose_name='provider')),
                ('video_key', models.CharField(verbose_name='key', blank=True, max_length=32)),
                ('video_preview', models.CharField(verbose_name='preview image', blank=True, max_length=128)),
            ],
            options={
                'verbose_name': 'video item',
                'verbose_name_plural': 'video items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='PostSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('alias', libs.autoslug.AutoSlugField(verbose_name='alias', populate_from='title', unique=True)),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='gallery',
            field=gallery.fields.GalleryField(verbose_name='gallery', to='posts.PostGallery', related_name='post_gallery', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='sections',
            field=models.ManyToManyField(verbose_name='sections', to='posts.PostSection'),
            preserve_default=True,
        ),
    ]
