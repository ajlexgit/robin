# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime
from django.conf import settings
import libs.stdimage.fields
import files.models
import libs.ckeditor.fields
import libs.media_storage
import gallery.fields
import posts.models
import libs.autoslug
import gallery.models
import files.fields
import libs.checks


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('alias', libs.autoslug.AutoSlugField(unique=True, populate_from='title', verbose_name='alias')),
                ('preview', libs.stdimage.fields.StdImageField(variations={'small': {'size': (140, 100)}, 'normal': {'size': (280, 200)}, 'big': {'action': 3, 'size': (800, 600), 'watermark': {'padding': (20, 20), 'file': 'img/watermark.png', 'opacity': 0.6}}}, min_dimensions=(280, 200), storage=libs.media_storage.MediaStorage('posts/preview'), aspects='normal', upload_to=posts.models.post_preview_filename, blank=True, verbose_name='preview')),
                ('note', libs.ckeditor.fields.CKEditorField(verbose_name='note')),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(verbose_name='date', default=datetime.datetime.now)),
                ('status', models.IntegerField(verbose_name='status', default=1, choices=[(1, 'Draft'), (2, 'Public')])),
                ('author', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, verbose_name='author')),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('file', files.fields.RemovableFileField(max_length=150, storage=libs.media_storage.MediaStorage(), upload_to=files.models.generate_filepath, verbose_name='file')),
                ('displayed_name', models.CharField(help_text='If you leave it empty the file name will be used', max_length=150, blank=True, verbose_name='display name')),
                ('order', models.PositiveIntegerField(verbose_name='order', blank=True, default=0)),
                ('post', models.ForeignKey(related_name='files', to='posts.Post', verbose_name='post')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='gallery.GalleryItemBase', serialize=False)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, null=True, blank=True, verbose_name='image')),
                ('crop', models.CharField(max_length=32, verbose_name='image crop coordinates')),
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
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='gallery.GalleryItemBase', serialize=False)),
                ('video_provider', models.PositiveSmallIntegerField(verbose_name='provider', default=0)),
                ('video_key', models.CharField(max_length=32, blank=True, verbose_name='key')),
                ('video_preview', models.CharField(max_length=128, blank=True, verbose_name='preview image')),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
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
            field=gallery.fields.GalleryField(null=True, related_name='post_gallery', on_delete=django.db.models.deletion.SET_NULL, to='posts.PostGallery', blank=True, verbose_name='gallery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='sections',
            field=models.ManyToManyField(to='posts.PostSection', verbose_name='sections'),
            preserve_default=True,
        ),
    ]
