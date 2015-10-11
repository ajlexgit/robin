# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import gallery.models
import django.core.validators
import gallery.fields
import ckeditor.fields
import files.models
import libs.stdimage.fields
import libs.valute_field.fields
import libs.media_storage
import libs.color_field.fields
import libs.videolink_field.fields
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, blank=True, verbose_name='title', default='Example')),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name', default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=150, upload_to=files.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='file')),
                ('displayed_name', models.CharField(help_text='If you leave it empty the file name will be used', max_length=150, blank=True, verbose_name='display name')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'files',
                'verbose_name': 'file',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True)),
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
                ('attachableblock_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='gallery.GalleryItemBase', primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, blank=True, verbose_name='stored_crop', editable=False)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='gallery.GalleryItemBase', primary_key=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'video items',
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), aspects=(), verbose_name='background', variations={'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}, 'admin': {'size': (360, 270)}}, upload_to='', min_dimensions=(1024, 500))),
                ('header_video', models.FileField(upload_to='', storage=libs.media_storage.MediaStorage('main/header'), blank=True, verbose_name='video')),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',), verbose_name='preview', variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, upload_to='', min_dimensions=(400, 300))),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',), verbose_name='preview', variations={'normal': {'size': (200, 200)}}, upload_to='', min_dimensions=(100, 100))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set(['youtube']), blank=True, verbose_name='video')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, verbose_name='gallery', to='main.MainGallery')),
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
