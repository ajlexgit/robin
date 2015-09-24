# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.db.models.deletion
import libs.checks
import gallery.fields
import libs.media_storage
import libs.color_field.fields
import libs.valute_field.fields
import gallery.models
import ckeditor.fields
import libs.videolink_field.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='title', blank=True, default='Example')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name', default='Test')),
                ('form', models.ForeignKey(to='main.ClientFormModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Second blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
                'abstract': False,
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='image')),
                ('crop', models.CharField(max_length=32, verbose_name='image crop coordinates')),
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
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('header_background', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/header'), aspects=(), variations={'admin': {'size': (360, 270)}, 'mobile': {'size': (768, 0)}, 'desktop': {'size': (1024, 0)}}, min_dimensions=(1024, 500), upload_to='', verbose_name='background')),
                ('header_video', models.FileField(upload_to='', storage=libs.media_storage.MediaStorage('main/header'), verbose_name='video', blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',), variations={'admin': {'size': (360, 270)}, 'normal': {'size': (800, 600)}}, min_dimensions=(400, 300), upload_to='', verbose_name='preview')),
                ('preview2', libs.stdimage.fields.StdImageField(storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',), variations={'normal': {'size': (200, 200)}}, min_dimensions=(100, 100), upload_to='', verbose_name='preview')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video', blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, null=True, to='main.MainGallery', verbose_name='gallery', blank=True)),
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
