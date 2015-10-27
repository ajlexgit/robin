# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import files.models
import google_maps.fields
import ckeditor.fields
import gallery.models
import libs.media_storage
import libs.stdimage.fields
import libs.valute_field.fields
import gallery.fields
import libs.color_field.fields
import libs.videolink_field.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(default='Example', verbose_name='title', max_length=128, blank=True)),
                ('image', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/client_images'), upload_to='', min_dimensions=(100, 100), verbose_name='image', aspects=('normal',), variations={'normal': {'size': (200, 200)}})),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default='Test', verbose_name='name', max_length=128)),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')])),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('file', models.FileField(upload_to=files.models.generate_filepath, verbose_name='file', storage=libs.media_storage.MediaStorage(), max_length=150)),
                ('displayed_name', models.CharField(help_text='If you leave it empty the file name will be used', verbose_name='display name', max_length=150, blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name_plural': 'files',
                'verbose_name': 'file',
                'abstract': False,
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True)),
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
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase', auto_created=True)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase', auto_created=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.media_storage.MediaStorage(), verbose_name='preview', upload_to=gallery.models.generate_filepath, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), upload_to='', min_dimensions=(1024, 500), verbose_name='background', aspects=(), variations={'desktop': {'size': (1024, 0)}, 'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}})),
                ('header_video', models.FileField(storage=libs.media_storage.MediaStorage('main/header'), verbose_name='video', upload_to='', blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), upload_to='', min_dimensions=(400, 300), verbose_name='preview', aspects=('normal',), blank=True, variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}})),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', min_dimensions=(100, 100), verbose_name='preview', aspects=('normal',), variations={'normal': {'size': (200, 200)}})),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set(['youtube']), blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='gallery', to='main.MainGallery', blank=True)),
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
