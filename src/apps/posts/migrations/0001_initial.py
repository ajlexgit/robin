# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.ckeditor.fields
import datetime
import files.fields
import files.models
import gallery.models
from django.conf import settings
import libs.autoslug
import django.db.models.deletion
import libs.media_storage
import libs.stdimage.fields
import libs.checks
import posts.models
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from='title', verbose_name='alias')),
                ('preview', libs.stdimage.fields.StdImageField(aspects='normal', blank=True, verbose_name='preview', variations={'small': {'size': (140, 100)}, 'big': {'watermark': {'padding': (20, 20), 'opacity': 0.6, 'file': 'img/watermark.png'}, 'size': (800, 600), 'action': 3}, 'normal': {'size': (280, 200)}}, storage=libs.media_storage.MediaStorage('posts/preview'), upload_to=posts.models.post_preview_filename, min_dimensions=(280, 200))),
                ('note', libs.ckeditor.fields.CKEditorField(verbose_name='note')),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='date')),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Public')], default=1, verbose_name='status')),
                ('author', models.ForeignKey(blank=True, null=True, verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', files.fields.RemovableFileField(storage=libs.media_storage.MediaStorage(), upload_to=files.models.generate_filepath, verbose_name='file', max_length=150)),
                ('displayed_name', models.CharField(blank=True, help_text='If you leave it empty the file name will be used', verbose_name='display name', max_length=150)),
                ('order', models.PositiveIntegerField(blank=True, verbose_name='order', default=0)),
                ('post', models.ForeignKey(related_name='files', to='posts.Post', verbose_name='post')),
            ],
            options={
                'verbose_name_plural': 'files',
                'abstract': False,
                'verbose_name': 'file',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, to='gallery.GalleryItemBase', primary_key=True, serialize=False, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), blank=True, verbose_name='image', null=True, upload_to=gallery.models.generate_filepath)),
                ('crop', models.CharField(verbose_name='image crop coordinates', max_length=32)),
            ],
            options={
                'verbose_name_plural': 'image items',
                'abstract': False,
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='PostGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, to='gallery.GalleryItemBase', primary_key=True, serialize=False, parent_link=True)),
                ('video_provider', models.PositiveSmallIntegerField(default=0, verbose_name='provider')),
                ('video_key', models.CharField(blank=True, verbose_name='key', max_length=32)),
                ('video_preview', models.CharField(blank=True, verbose_name='preview image', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'video items',
                'abstract': False,
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='PostSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from='title', verbose_name='alias')),
            ],
            options={
                'verbose_name_plural': 'sections',
                'verbose_name': 'section',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='gallery',
            field=gallery.fields.GalleryField(related_name='post_gallery', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', to='posts.PostGallery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='sections',
            field=models.ManyToManyField(to='posts.PostSection', verbose_name='sections'),
            preserve_default=True,
        ),
    ]
