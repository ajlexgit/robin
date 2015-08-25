# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import libs.media_storage
import libs.color_field.fields
import gallery.models
import django.db.models.deletion
import libs.stdimage.fields
import libs.valute_field.fields
import libs.ckeditor.fields
import gallery.fields
import libs.checks


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
        ('attachable_blocks', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, default='Example', verbose_name='title')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientInlineFormModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, serialize=False, to='attachable_blocks.AttachableBlock', parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'First blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='MainBlockSecond',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, serialize=False, to='attachable_blocks.AttachableBlock', parent_link=True, primary_key=True)),
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
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, serialize=False, to='gallery.GalleryItemBase', parent_link=True, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(null=True, blank=True, storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('crop', models.CharField(max_length=32, verbose_name='image crop coordinates')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('header_title', models.CharField(max_length=255, verbose_name='title')),
                ('preview', libs.stdimage.fields.StdImageField(min_dimensions=(400, 300), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview'), upload_to='', verbose_name='preview')),
                ('preview2', libs.stdimage.fields.StdImageField(min_dimensions=(100, 100), variations={'normal': {'action': 3, 'size': (140, 140)}}, aspects=('normal',), storage=libs.media_storage.MediaStorage('main/preview2'), upload_to='', verbose_name='preview')),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', libs.color_field.fields.ColorField(blank=True, verbose_name='color')),
                ('color2', libs.color_field.fields.ColorOpacityField(blank=True, verbose_name='color2')),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='main.MainGallery', null=True, verbose_name='gallery')),
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
