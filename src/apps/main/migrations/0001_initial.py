# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models
import gallery.fields
import django.db.models.deletion
import libs.storages.media_storage
import libs.stdimage.fields
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, to='gallery.GalleryItemBase', auto_created=True, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage())),
                ('image_crop', models.CharField(editable=False, verbose_name='stored_crop', blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'image items',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), upload_to='', storage=libs.storages.media_storage.MediaStorage('main'), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, verbose_name='preview', blank=True, min_dimensions=(800, 600))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(to='main.Gallery', verbose_name='gallery', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(parent_link=True, serialize=False, to='gallery.GalleryItemBase', auto_created=True, primary_key=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage(), blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'video items',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
