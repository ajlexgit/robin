# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.fields
import libs.stdimage.fields
import libs.color_field.fields
import django.db.models.deletion
import libs.videolink_field.fields
import ckeditor.fields
import django.core.validators
import libs.valute_field.fields
import libs.media_storage
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        ('attachable_blocks', '0002_auto_20150927_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=128, default='Example')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=128, default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('attachableblock_ptr', models.OneToOneField(serialize=False, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, auto_created=True, to='attachable_blocks.AttachableBlock', primary_key=True, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, auto_created=True, to='gallery.GalleryItemBase', primary_key=True, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(blank=True, verbose_name='stored_crop', max_length=32, editable=False)),
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
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, auto_created=True, to='gallery.GalleryItemBase', primary_key=True, parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, verbose_name='preview', storage=libs.media_storage.MediaStorage())),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(verbose_name='background', min_dimensions=(1024, 500), aspects=(), variations={'admin': {'size': (360, 270)}, 'desktop': {'size': (1024, 0)}, 'mobile': {'size': (768, 0)}}, upload_to='', storage=libs.media_storage.MediaStorage('main/header'))),
                ('header_video', models.FileField(blank=True, verbose_name='video', upload_to='', storage=libs.media_storage.MediaStorage('main/header'))),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(400, 300), aspects=('normal',), variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, upload_to='', storage=libs.media_storage.MediaStorage('main/preview'))),
                ('preview2', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(100, 100), aspects=('normal',), variations={'normal': {'size': (200, 200)}}, upload_to='', storage=libs.media_storage.MediaStorage('main/preview2'))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('video', libs.videolink_field.fields.VideoLinkField(blank=True, verbose_name='video', providers=set([]))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(blank=True, verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, to='main.MainGallery', null=True)),
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
