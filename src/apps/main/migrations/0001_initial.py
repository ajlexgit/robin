# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import gallery.models
import gallery.fields
import django.db.models.deletion
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'default_permissions': (),
                'abstract': False,
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='image')),
                ('image_crop', models.CharField(blank=True, verbose_name='stored_crop', max_length=32, editable=False)),
            ],
            options={
                'default_permissions': (),
                'abstract': False,
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), storage=libs.media_storage.MediaStorage('main'), min_dimensions=(800, 600), variations={'normal': {'size': (800, 600)}, 'admin': {'size': (280, 280)}}, upload_to='', blank=True, verbose_name='preview')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', blank=True, null=True, to='main.Gallery')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(blank=True, storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath, verbose_name='preview')),
            ],
            options={
                'default_permissions': (),
                'abstract': False,
                'verbose_name_plural': 'video items',
                'verbose_name': 'video item',
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
