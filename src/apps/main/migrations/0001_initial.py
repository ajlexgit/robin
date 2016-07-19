# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models
import gallery.fields
import libs.stdimage.fields
import libs.storages.media_storage
import django.db.models.deletion
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
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
                'default_permissions': (),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='gallery.GalleryItemBase', primary_key=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', storage=libs.storages.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
                ('image_crop', models.CharField(verbose_name='stored_crop', blank=True, max_length=32, editable=False)),
            ],
            options={
                'verbose_name': 'image item',
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'image items',
                'default_permissions': (),
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage('main'), blank=True, variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, min_dimensions=(800, 600), aspects=('normal',), upload_to='')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='gallery.GalleryItemBase', primary_key=True)),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.storages.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'video items',
                'default_permissions': (),
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
