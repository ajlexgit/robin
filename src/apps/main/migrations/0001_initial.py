# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import libs.stdimage.fields
import django.db.models.deletion
import gallery.models
import libs.media_storage
import libs.checks
import libs.ckeditor.fields
import libs.valute_field.fields
import django.core.validators
import gallery.fields
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InlineSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', libs.color_field.fields.ColorOpacityField(verbose_name='color')),
            ],
            options={
                'verbose_name': 'Inline sample',
                'verbose_name_plural': 'Inline samples',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
            bases=(libs.checks.ModelChecksMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainGalleryImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, blank=True, storage=libs.media_storage.MediaStorage(), null=True)),
                ('crop', models.CharField(verbose_name='image crop coordinates', max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header_title', models.CharField(verbose_name='title', max_length=255)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', variations={'normal': {'size': (800, 600)}, 'admin': {'size': (360, 270)}}, upload_to='', storage=libs.media_storage.MediaStorage('main/preview'), min_dimensions=(400, 300), aspects=('normal',))),
                ('text', libs.ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', libs.color_field.fields.ColorField(verbose_name='color', blank=True)),
                ('color2', libs.color_field.fields.ColorOpacityField(verbose_name='color2', blank=True)),
                ('price', libs.valute_field.fields.ValuteField(verbose_name='price', validators=[django.core.validators.MinValueValidator(0)])),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', to='main.MainGallery', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True)),
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
