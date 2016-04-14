# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.fields
import libs.media_storage
import django.db.models.deletion
import libs.videolink_field.fields
import libs.stdimage.fields
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'default_permissions': (),
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, verbose_name='image', storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(max_length=32, blank=True, verbose_name='stored_crop', editable=False)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'image items',
                'default_permissions': (),
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), min_dimensions=(800, 600), upload_to='', verbose_name='preview', variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, storage=libs.media_storage.MediaStorage('main'), blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(null=True, verbose_name='gallery', to='main.Gallery', on_delete=django.db.models.deletion.SET_NULL, blank=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(upload_to=gallery.models.generate_filepath, verbose_name='preview', storage=libs.media_storage.MediaStorage(), blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'video items',
                'default_permissions': (),
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
