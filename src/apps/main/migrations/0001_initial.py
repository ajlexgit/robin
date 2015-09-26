# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.videolink_field.fields
import libs.media_storage
import libs.color_field.fields
import gallery.models
import gallery.fields
import libs.valute_field.fields
import ckeditor.fields
import django.db.models.deletion
import libs.stdimage.fields
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', blank=True, default='Example', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', default='Test', max_length=128)),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='attachable_blocks.AttachableBlock')),
            ],
            options={
                'verbose_name_plural': 'First blocks',
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
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(editable=False, verbose_name='stored_crop', blank=True, max_length=32)),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(aspects=(), min_dimensions=(1024, 500), verbose_name='background', variations={'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}, 'admin': {'size': (360, 270)}}, storage=libs.media_storage.MediaStorage('main/header'), upload_to='')),
                ('header_video', models.FileField(verbose_name='video', blank=True, storage=libs.media_storage.MediaStorage('main/header'), upload_to='')),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), min_dimensions=(400, 300), verbose_name='preview', variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, storage=libs.media_storage.MediaStorage('main/preview'), upload_to='')),
                ('preview2', libs.stdimage.fields.StdImageField(aspects=('normal',), min_dimensions=(100, 100), verbose_name='preview', variations={'normal': {'size': (200, 200)}}, storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', blank=True, providers=set([]))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(null=True, verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.MainGallery')),
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
