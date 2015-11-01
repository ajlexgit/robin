# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.fields
import files.models
import google_maps.fields
import django.db.models.deletion
import django.core.validators
import libs.color_field.fields
import libs.media_storage
import libs.videolink_field.fields
import libs.valute_field.fields
import gallery.models
import yandex_maps.fields
import ckeditor.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=128, blank=True, default='Example')),
                ('image', libs.stdimage.fields.StdImageField(verbose_name='image', upload_to='', min_dimensions=(100, 100), storage=libs.media_storage.MediaStorage('main/client_images'), aspects=('normal',), variations={'normal': {'size': (200, 200)}})),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True)),
                ('coords2', yandex_maps.fields.YandexCoordsField(verbose_name='coords2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=128, default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')])),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file', models.FileField(verbose_name='file', storage=libs.media_storage.MediaStorage(), max_length=150, upload_to=files.models.generate_filepath)),
                ('displayed_name', models.CharField(verbose_name='display name', help_text='If you leave it empty the file name will be used', max_length=150, blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name': 'file',
                'ordering': ('sort_order',),
                'verbose_name_plural': 'files',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name': 'First block',
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name': 'Second block',
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(verbose_name='background', upload_to='', min_dimensions=(1024, 500), storage=libs.media_storage.MediaStorage('main/header'), aspects=(), variations={'admin': {'size': (360, 270)}, 'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}})),
                ('header_video', models.FileField(verbose_name='video', storage=libs.media_storage.MediaStorage('main/header'), upload_to='', blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', upload_to='', min_dimensions=(400, 300), storage=libs.media_storage.MediaStorage('main/preview'), blank=True, variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, aspects=('normal',))),
                ('preview2', libs.stdimage.fields.StdImageField(verbose_name='preview', upload_to='', min_dimensions=(100, 100), storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',), variations={'normal': {'size': (200, 200)}})),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', choices=[('#FFFFFF', 'white'), ('#FF0000', 'red'), ('#00FF00', 'green'), ('#0000FF', 'blue'), ('#FFFF00', 'yellow'), ('#000000', 'black')])),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True)),
                ('coords2', yandex_maps.fields.YandexCoordsField(verbose_name='coords2', blank=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', blank=True, providers=set(['youtube']))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', null=True, to='main.MainGallery', blank=True, on_delete=django.db.models.deletion.SET_NULL)),
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
