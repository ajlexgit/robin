# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import gallery.models
import gallery.fields
import django.db.models.deletion
import libs.videolink_field.fields
import libs.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, blank=True, editable=False, verbose_name='stored_crop')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', libs.stdimage.fields.StdImageField(min_dimensions=(800, 600), variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, storage=libs.media_storage.MediaStorage('main'), upload_to='', verbose_name='preview', blank=True, aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, auto_created=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(blank=True, upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage(), verbose_name='preview')),
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
