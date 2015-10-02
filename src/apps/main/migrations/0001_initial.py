# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import google_maps.fields
import django.core.validators
import files.models
import gallery.fields
import gallery.models
import libs.color_field.fields
import libs.valute_field.fields
import libs.videolink_field.fields
import django.db.models.deletion
import libs.media_storage
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='title', default='Example')),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name', default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('color', libs.color_field.fields.ColorOpacityField(verbose_name='color')),
            ],
            options={
                'verbose_name_plural': 'Inline samples',
                'verbose_name': 'Inline sample',
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(upload_to=files.models.generate_filepath, max_length=150, storage=libs.media_storage.MediaStorage(), verbose_name='file')),
                ('displayed_name', models.CharField(blank=True, max_length=150, help_text='If you leave it empty the file name will be used', verbose_name='display name')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name_plural': 'files',
                'ordering': ('sort_order',),
                'abstract': False,
                'verbose_name': 'file',
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='attachable_blocks.AttachableBlock', parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='attachable_blocks.AttachableBlock', parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase', parent_link=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(editable=False, blank=True, max_length=32, verbose_name='stored_crop')),
            ],
            options={
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase', parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
            ],
            options={
                'verbose_name_plural': 'video items',
                'verbose_name': 'video item',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('header_background', libs.stdimage.fields.StdImageField(variations={'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}, 'desktop': {'size': (1024, 0)}}, storage=libs.media_storage.MediaStorage('main/header'), aspects=(), upload_to='', verbose_name='background', min_dimensions=(1024, 500))),
                ('header_video', models.FileField(upload_to='', blank=True, storage=libs.media_storage.MediaStorage('main/header'), verbose_name='video')),
                ('preview', libs.stdimage.fields.StdImageField(variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',), upload_to='', verbose_name='preview', min_dimensions=(400, 300))),
                ('preview2', libs.stdimage.fields.StdImageField(variations={'normal': {'size': (200, 200)}}, storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',), upload_to='', verbose_name='preview', min_dimensions=(100, 100))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords')),
                ('video', libs.videolink_field.fields.VideoLinkField(blank=True, providers=set([]), verbose_name='video')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.MainGallery', null=True, verbose_name='gallery')),
            ],
            options={
                'verbose_name': 'Settings',
            },
        ),
        migrations.AddField(
            model_name='inlinesample',
            name='config',
            field=models.ForeignKey(to='main.MainPageConfig', verbose_name='config'),
        ),
    ]
