# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.checks
import libs.valute_field.fields
import ckeditor.fields
import libs.stdimage.fields
import django.core.validators
import django.db.models.deletion
import gallery.fields
import libs.media_storage
import gallery.models
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '__first__'),
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(default='Example', verbose_name='title', max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('color', libs.color_field.fields.ColorOpacityField(verbose_name='color')),
            ],
            options={
                'verbose_name_plural': 'Inline samples',
                'verbose_name': 'Inline sample',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainBlockFirst',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', serialize=False, primary_key=True)),
            ],
            options={
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
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='gallery.GalleryItemBase', serialize=False, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, null=True, verbose_name='image', storage=libs.media_storage.MediaStorage(), blank=True)),
                ('crop', models.CharField(verbose_name='image crop coordinates', max_length=32)),
            ],
            options={
                'verbose_name_plural': 'image items',
                'abstract': False,
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('header_background', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(1024, 500), variations={'mobile': {'stretch': False, 'size': (640, 0), 'crop': False}, 'admin': {'size': (360, 270)}, 'desktop': {'stretch': False, 'size': (1024, 0), 'crop': False}}, verbose_name='background', storage=libs.media_storage.MediaStorage('main/header'), aspects=())),
                ('header_video', models.FileField(upload_to='', verbose_name='video', storage=libs.media_storage.MediaStorage('main/header'), blank=True)),
                ('preview', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(400, 300), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, verbose_name='preview', storage=libs.media_storage.MediaStorage('main/preview'), aspects=('normal',))),
                ('preview2', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(100, 100), variations={'normal': {'size': (200, 200)}}, verbose_name='preview', storage=libs.media_storage.MediaStorage('main/preview2'), aspects=('normal',))),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(null=True, to='main.MainGallery', on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', blank=True)),
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
