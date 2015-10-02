# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import gallery.models
import files.models
import gallery.fields
import libs.color_field.fields
import libs.videolink_field.fields
import google_maps.fields
import django.db.models.deletion
import libs.media_storage
import libs.stdimage.fields
import libs.valute_field.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', blank=True, default='Example', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', default='Test', max_length=128)),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('color', libs.color_field.fields.ColorOpacityField(verbose_name='color')),
            ],
            options={
                'verbose_name': 'Inline sample',
                'verbose_name_plural': 'Inline samples',
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('file', models.FileField(storage=libs.media_storage.MediaStorage(), verbose_name='file', upload_to=files.models.generate_filepath, max_length=150)),
                ('displayed_name', models.CharField(verbose_name='display name', blank=True, help_text='If you leave it empty the file name will be used', max_length=150)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'abstract': False,
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', editable=False, blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
            ],
            options={
                'verbose_name': 'video item',
                'verbose_name_plural': 'video items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(verbose_name='background', aspects=(), storage=libs.media_storage.MediaStorage('main/header'), upload_to='', variations={'mobile': {'size': (768, 0)}, 'admin': {'size': (360, 270)}, 'desktop': {'size': (1024, 0)}}, min_dimensions=(1024, 500))),
                ('header_video', models.FileField(verbose_name='video', blank=True, storage=libs.media_storage.MediaStorage('main/header'), upload_to='')),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview'), upload_to='', variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, min_dimensions=(400, 300))),
                ('preview2', libs.stdimage.fields.StdImageField(verbose_name='preview', aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', variations={'normal': {'size': (200, 200)}}, min_dimensions=(100, 100))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', blank=True, providers=set([]))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(to='main.MainGallery', verbose_name='gallery', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.AddField(
            model_name='inlinesample',
            name='config',
            field=models.ForeignKey(verbose_name='config', to='main.MainPageConfig'),
        ),
    ]
