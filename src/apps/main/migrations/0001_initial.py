# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models
import libs.stdimage.fields
import libs.videolink_field.fields
import libs.media_storage
import gallery.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(editable=False, verbose_name='stored_crop', blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'default_permissions': (),
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('preview', libs.stdimage.fields.StdImageField(verbose_name='preview', storage=libs.media_storage.MediaStorage('main'), blank=True, aspects=('normal',), upload_to='', variations={'admin': {'size': (280, 280)}, 'normal': {'size': (800, 600)}}, min_dimensions=(800, 600))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(verbose_name='gallery', blank=True, null=True, to='main.Gallery', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(to='gallery.GalleryItemBase', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set([]))),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, blank=True)),
            ],
            options={
                'verbose_name': 'video item',
                'verbose_name_plural': 'video items',
                'default_permissions': (),
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
