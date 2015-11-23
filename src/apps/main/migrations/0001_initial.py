# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields
import ckeditor.fields
import libs.valute_field.fields
import libs.color_field.fields
import gallery.fields
import libs.media_storage
import files.models
import libs.stdimage.fields
import gallery.models
import django.db.models.deletion
import google_maps.fields
import django.core.validators
import yandex_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128, blank=True, verbose_name='title', default='Example')),
                ('image', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/client_images'), verbose_name='image', aspects=('normal',), min_dimensions=(100, 100), variations={'normal': {'size': (200, 200)}}, upload_to='')),
                ('count', models.PositiveIntegerField(verbose_name='count', default=1, validators=[django.core.validators.MaxValueValidator(99)])),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords')),
                ('coords2', yandex_maps.fields.YandexCoordsField(blank=True, verbose_name='coords2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('visible', models.BooleanField(verbose_name='visible', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, verbose_name='name', default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='ListItemFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('file', models.FileField(storage=libs.media_storage.MediaStorage(), max_length=150, verbose_name='file', upload_to=files.models.generate_filepath)),
                ('displayed_name', models.CharField(max_length=150, blank=True, verbose_name='display name', help_text='If you leave it empty the file name will be used')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('item', models.ForeignKey(to='main.ListItem')),
            ],
            options={
                'verbose_name_plural': 'files',
                'abstract': False,
                'ordering': ('sort_order',),
                'verbose_name': 'file',
            },
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='attachable_blocks.AttachableBlock')),
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
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='attachable_blocks.AttachableBlock')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(max_length=32, blank=True, editable=False, verbose_name='stored_crop')),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.media_storage.MediaStorage(), blank=True, verbose_name='preview', upload_to=gallery.models.generate_filepath)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), verbose_name='background', aspects=(), min_dimensions=(1024, 500), variations={'admin': {'size': (360, 270)}, 'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}}, upload_to='')),
                ('header_video', models.FileField(storage=libs.media_storage.MediaStorage('main/header'), blank=True, verbose_name='video', upload_to='')),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), verbose_name='preview', aspects=('normal',), min_dimensions=(400, 300), blank=True, variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, upload_to='')),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), verbose_name='preview', aspects=('normal',), min_dimensions=(100, 100), variations={'normal': {'size': (200, 200)}}, upload_to='')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(choices=[('#FFFFFF', 'white'), ('#FF0000', 'red'), ('#00FF00', 'green'), ('#0000FF', 'blue'), ('#FFFF00', 'yellow'), ('#000000', 'black')], verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('coords', google_maps.fields.GoogleCoordsField(blank=True, verbose_name='coords')),
                ('coords2', yandex_maps.fields.YandexCoordsField(blank=True, verbose_name='coords2')),
                ('video', libs.videolink_field.fields.VideoLinkField(blank=True, verbose_name='video', providers=set(['youtube']))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.MainGallery')),
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
