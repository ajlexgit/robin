# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gallery.fields
import libs.storages.media_storage
import gallery.models
import libs.videolink_field.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(max_length=32, editable=False, blank=True, verbose_name='stored_crop')),
            ],
            options={
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'image items',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('preview', libs.stdimage.fields.StdImageField(upload_to='', min_dimensions=(800, 600), blank=True, verbose_name='preview', variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, storage=libs.storages.media_storage.MediaStorage('main'), aspects=('normal',))),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', null=True, to='main.Gallery', blank=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, parent_link=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(storage=libs.storages.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, blank=True, verbose_name='preview')),
            ],
            options={
                'ordering': ('object_id', 'sort_order', 'created'),
                'verbose_name_plural': 'video items',
                'abstract': False,
                'default_permissions': (),
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
