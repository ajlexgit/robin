# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import files.models
import libs.videolink_field.fields
import django.core.validators
import libs.media_storage
import google_maps.fields
import gallery.models
import libs.valute_field.fields
import django.db.models.deletion
import libs.stdimage.fields
import libs.color_field.fields
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=128, default='Example')),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=128, default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('file', models.FileField(storage=libs.media_storage.MediaStorage(), verbose_name='file', max_length=150, upload_to=files.models.generate_filepath)),
                ('displayed_name', models.CharField(blank=True, help_text='If you leave it empty the file name will be used', verbose_name='display name', max_length=150)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name_plural': 'files',
                'abstract': False,
                'verbose_name': 'file',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
                'verbose_name': 'First block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
                'verbose_name': 'Second block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(editable=False, blank=True, verbose_name='stored_crop', max_length=32)),
            ],
            options={
                'verbose_name_plural': 'image items',
                'abstract': False,
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
            ],
            options={
                'verbose_name_plural': 'video items',
                'abstract': False,
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(verbose_name='background', min_dimensions=(1024, 500), variations={'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}, 'desktop': {'size': (1024, 0)}}, aspects=(), storage=libs.media_storage.MediaStorage('main/header'), upload_to='')),
                ('header_video', models.FileField(blank=True, verbose_name='video', storage=libs.media_storage.MediaStorage('main/header'), upload_to='')),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(400, 300), variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview'), upload_to='')),
                ('preview2', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(100, 100), variations={'normal': {'size': (200, 200)}}, aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), blank=True, verbose_name='video')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, to='main.MainGallery', verbose_name='gallery', null=True, blank=True)),
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
