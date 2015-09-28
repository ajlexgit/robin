# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models
import libs.color_field.fields
import gallery.fields
import libs.stdimage.fields
import libs.valute_field.fields
import django.db.models.deletion
import django.core.validators
import libs.videolink_field.fields
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(blank=True, default='Example', verbose_name='title', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('color', libs.color_field.fields.ColorOpacityField(verbose_name='color')),
            ],
            options={
                'verbose_name': 'Inline sample',
                'verbose_name_plural': 'Inline samples',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=64)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
                'verbose_name': 'gallery',
                'abstract': False,
                'verbose_name_plural': 'galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(blank=True, verbose_name='stored_crop', editable=False, max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'abstract': False,
                'verbose_name_plural': 'image items',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainGalleryVideoLinkItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, verbose_name='preview', storage=libs.media_storage.MediaStorage())),
            ],
            options={
                'verbose_name': 'video item',
                'abstract': False,
                'verbose_name_plural': 'video items',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(min_dimensions=(1024, 500), storage=libs.media_storage.MediaStorage('main/header'), upload_to='', verbose_name='background', variations={'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}, 'desktop': {'size': (1024, 0)}}, aspects=())),
                ('header_video', models.FileField(blank=True, upload_to='', verbose_name='video', storage=libs.media_storage.MediaStorage('main/header'))),
                ('preview', libs.stdimage.fields.StdImageField(min_dimensions=(400, 300), storage=libs.media_storage.MediaStorage('main/preview'), upload_to='', verbose_name='preview', variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, aspects=('normal',))),
                ('preview2', libs.stdimage.fields.StdImageField(min_dimensions=(100, 100), storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', verbose_name='preview', variations={'normal': {'size': (200, 200)}}, aspects=('normal',))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('text2', ckeditor.fields.CKEditorUploadField(verbose_name='text2')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('video', libs.videolink_field.fields.VideoLinkField(blank=True, verbose_name='video', providers=set([]))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(blank=True, to='main.MainGallery', null=True, verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inlinesample',
            name='config',
            field=models.ForeignKey(to='main.MainPageConfig', verbose_name='config'),
            preserve_default=True,
        ),
    ]
