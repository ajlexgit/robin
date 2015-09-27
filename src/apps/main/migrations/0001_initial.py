# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.color_field.fields
import libs.videolink_field.fields
import libs.valute_field.fields
import gallery.models
import django.core.validators
import libs.media_storage
import libs.stdimage.fields
import gallery.fields
import django.db.models.deletion
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=128, default='Example', blank=True, verbose_name='title')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=128, default='Test', verbose_name='name')),
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
                'verbose_name_plural': 'Inline samples',
                'verbose_name': 'Inline sample',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid'), (3, 'Deleted')], default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='attachable_blocks.AttachableBlock')),
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
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, editable=False, verbose_name='stored_crop', blank=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='preview')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), min_dimensions=(1024, 500), aspects=(), variations={'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}, 'admin': {'size': (360, 270)}}, upload_to='', verbose_name='background')),
                ('header_video', models.FileField(storage=libs.media_storage.MediaStorage('main/header'), upload_to='', verbose_name='video', blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), min_dimensions=(400, 300), aspects=('normal',), variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, upload_to='', verbose_name='preview')),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), min_dimensions=(100, 100), aspects=('normal',), variations={'normal': {'size': (200, 200)}}, upload_to='', verbose_name='preview')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('text2', ckeditor.fields.CKEditorUploadField(verbose_name='text2')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video', blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, verbose_name='gallery', to='main.MainGallery')),
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
