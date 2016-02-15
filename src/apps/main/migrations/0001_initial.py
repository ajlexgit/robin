# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.media_storage
import django.db.models.deletion
import gallery.fields
import gallery.models
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'verbose_name_plural': 'galleries',
                'verbose_name': 'gallery',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, serialize=False, to='gallery.GalleryItemBase')),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.media_storage.MediaStorage())),
                ('image_crop', models.CharField(verbose_name='stored_crop', max_length=32, blank=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'image items',
                'verbose_name': 'image item',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='MainPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(to='main.Gallery', blank=True, verbose_name='gallery', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='VideoItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, serialize=False, to='gallery.GalleryItemBase')),
                ('video', libs.videolink_field.fields.VideoLinkField(providers=set([]), verbose_name='video')),
                ('video_preview', gallery.fields.GalleryVideoLinkPreviewField(verbose_name='preview', blank=True, storage=libs.media_storage.MediaStorage(), upload_to=gallery.models.generate_filepath)),
            ],
            options={
                'verbose_name_plural': 'video items',
                'verbose_name': 'video item',
                'abstract': False,
            },
            bases=('gallery.galleryitembase',),
        ),
    ]
