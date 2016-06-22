# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import libs.videolink_field.fields
import gallery.fields
import gallery.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, to='gallery.GalleryItemBase', auto_created=True, primary_key=True, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', blank=True, max_length=32, editable=False)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage('main'), upload_to='', min_dimensions=(800, 600), blank=True, variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, aspects=('normal',))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, to='gallery.GalleryItemBase', auto_created=True, primary_key=True, parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'verbose_name_plural': 'video items',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
