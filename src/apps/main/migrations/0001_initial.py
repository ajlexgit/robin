# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import ckeditor.fields
import libs.valute_field.fields
import libs.checks
import libs.color_field.fields
import django.db.models.deletion
import gallery.fields
import libs.videolink_field.fields
import gallery.models
import libs.media_storage
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(default='Example', blank=True, verbose_name='title', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(default='Test', verbose_name='name', max_length=128)),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
            options={
            },
            bases=(models.Model,),
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
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
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='image')),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
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
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), variations={'mobile': {'size': (768, 0)}, 'desktop': {'size': (1024, 0)}, 'admin': {'size': (360, 270)}}, upload_to='', min_dimensions=(1024, 500), verbose_name='background', aspects=())),
                ('header_video', models.FileField(upload_to='', storage=libs.media_storage.MediaStorage('main/header'), blank=True, verbose_name='video')),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, upload_to='', min_dimensions=(400, 300), verbose_name='preview', aspects=('normal',))),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), variations={'normal': {'size': (200, 200)}}, upload_to='', min_dimensions=(100, 100), verbose_name='preview', aspects=('normal',))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('video', libs.videolink_field.fields.VideoLinkField(blank=True, verbose_name='video', providers=set([]))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', to='main.MainGallery')),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inlinesample',
            name='config',
            field=models.ForeignKey(verbose_name='config', to='main.MainPageConfig'),
            preserve_default=True,
        ),
    ]
