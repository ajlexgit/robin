# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.valute_field.fields
import libs.stdimage.fields
import libs.videolink_field.fields
import libs.media_storage
import gallery.models
import django.db.models.deletion
import libs.color_field.fields
import django.core.validators
import ckeditor.fields
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=128, default='Example', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', default='Test', max_length=128)),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')])),
            ],
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='attachable_blocks.AttachableBlock', auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', editable=False, max_length=32, blank=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.media_storage.MediaStorage(), verbose_name='preview', upload_to=gallery.models.generate_filepath)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(verbose_name='background', variations={'desktop': {'size': (1024, 0)}, 'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}}, storage=libs.media_storage.MediaStorage('main/header'), min_dimensions=(1024, 500), upload_to='', aspects=())),
                ('header_video', models.FileField(storage=libs.media_storage.MediaStorage('main/header'), verbose_name='video', upload_to='', blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, storage=libs.media_storage.MediaStorage('main/preview'), min_dimensions=(400, 300), upload_to='', aspects=('normal',))),
                ('preview2', libs.stdimage.fields.StdImageField(verbose_name='preview', variations={'normal': {'size': (200, 200)}}, storage=libs.media_storage.MediaStorage('main/preview2'), min_dimensions=(100, 100), upload_to='', aspects=('normal',))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video', blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', to='main.MainGallery', on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True)),
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
