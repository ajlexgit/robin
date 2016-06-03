# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import libs.videolink_field.fields
import gallery.models
import libs.storages.media_storage
import libs.stdimage.fields
import gallery.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'verbose_name': 'gallery',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='gallery.GalleryItemBase', serialize=False)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage())),
                ('image_crop', models.CharField(blank=True, max_length=32, verbose_name='stored_crop', editable=False)),
            ],
            options={
                'verbose_name_plural': 'image items',
                'abstract': False,
                'verbose_name': 'image item',
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', min_dimensions=(800, 600), storage=libs.storages.media_storage.MediaStorage('main'), blank=True, variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, upload_to='', aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', blank=True, null=True, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='gallery.GalleryItemBase', serialize=False)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(blank=True, verbose_name='preview', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage())),
            ],
            options={
                'verbose_name_plural': 'video items',
                'abstract': False,
                'verbose_name': 'video item',
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
