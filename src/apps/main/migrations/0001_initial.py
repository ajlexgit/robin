# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models
import libs.stdimage.fields
import gallery.fields
import libs.storages.media_storage
import django.db.models.deletion
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'default_permissions': (),
                'verbose_name_plural': 'galleries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(storage=libs.storages.media_storage.MediaStorage(), verbose_name='image', upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(editable=False, verbose_name='stored_crop', max_length=32, blank=True)),
            ],
            options={
                'verbose_name': 'image item',
                'default_permissions': (),
                'verbose_name_plural': 'image items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('preview', libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('main'), verbose_name='preview', upload_to='', variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, aspects=('normal',), min_dimensions=(800, 600), blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', null=True, to='main.Gallery', blank=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, to='gallery.GalleryItemBase', auto_created=True, serialize=False, parent_link=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.storages.media_storage.MediaStorage(), verbose_name='preview', upload_to=gallery.models.generate_filepath, blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'default_permissions': (),
                'verbose_name_plural': 'video items',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
